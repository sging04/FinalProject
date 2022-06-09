#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, request, redirect, session, render_template, \
    url_for, jsonify, send_from_directory
import json
import os
import sqlite3
import requests as r
from database import UsernamePasswordTable, QuestionSetTable  # using database classes

# misc imports

import pytesseract
from werkzeug.utils import secure_filename
import os
import json
import csv
#######################
# api stuff

from setup import TESSERACT_LOCATION, UPLOAD_FOLDER

# --------
# config stuffs dont touch!

app = Flask(__name__)
app.secret_key = os.urandom(32)

db_file = 'data.db'

pytesseract.pytesseract.tesseract_cmd = UPLOAD_FOLDER
# might make a config file for this ^^^ will update

UPLOAD_FOLDER = "./uploads"
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

userpass = UsernamePasswordTable(db_file, 'userpass')
decks = QuestionSetTable(db_file, 'decks')


# ---------

# Utility function to check if there is a session

def logged_in():
    return  not (session.get('username') is None)


@app.route('/', methods=['GET'])
def landing():
    if logged_in():
        return redirect("/home")
    else:
        return render_template("login.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    method = request.method

    # Check for session existance

    if method == 'GET':
        if logged_in():
            return redirect(url_for('landing'))
        else:

        # If not logged in, show login page
            return render_template('login.html', error=False)

    if method == 'POST':

      # Get information from request.form since it is submitted via post

        username = request.form['username']
        password = request.form['password']


        if userpass.passMatch(username, password):

	        # If incorrect, give feedback to the user

	        session['username'] = username
	        return redirect(url_for('landing'))

        else:
	        return render_template('login.html',
	        					   isError=True,
	                               error='Username or Password are Incorrect'
	                               )


@app.route('/signup', methods=['GET', 'POST'])
def register():
    method = request.method

    # Check for session existence

    if method == 'GET':
        if logged_in():
            return redirect(url_for('landing'))
        else:

            # If not logged in, show regsiter page

            return render_template('signup.html', error_message='')

    if method == 'POST':
        username = request.form['new_username']
        password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        error_message = ''
        if not username:
            error_message = 'Error: No username entered!'
        elif not password:
            error_message = 'Error: No password entered!'
        elif confirm_password != password:
            error_message = 'Error: Passwords do not match!'

        if error_message:
            return render_template('signup.html',
                                   error_message=error_message)
        else:

            userpass.insert(username, password)

            session['username'] = username
            return redirect(url_for('landing'))


# @app.route("/signup", methods=["POST","GET"])
# def signup():
#     if session['username'] is not none:
#         redirect("/")
#     if request.method == "GET":
#         return render_template("signup.html")
#     elif request.method == "POST":
#         username= request.args['username']
#         password= request.args['password']
#         passauth= request.args['passauth']
#         userpass.insert(username, password) # committing actions to database must be done every time you commit a command
#         session["username"]=username
#         return redirect("/home", username=session.get("username"))

@app.route('/home', methods=['GET'])
def home():
	if logged_in():
		return render_template('home.html', username=session.get('username'), decks=decks.getRandomEntries(10))

	return redirect("/")

@app.route('/logout', methods=['GET', 'POST'])
def logout():

    # Once again check for a key before popping it

    if logged_in():
        session.pop('username')

    # After logout, return to login page

    return redirect("/")

@app.route("/search", methods=["GET","POST"])
def search():

	if request.method == "GET":
		return redirect("/home")

	query = request.form.get("query")

	results = decks.search(query)

	return render_template("search.html", length = len(results), results=results)

@app.route("/addDeck", methods=["POST"])
def addDeck():
	'''
	Insert in the code from the form when it comes
	'''
	if logged_in():
		title = ""
		description = ""
		content = ""
		decks.insert(
			title,
			session.get("username"),
			description,
			content
			)

		return redirect("/home")

@app.route('/create', methods=['GET'])
def create():
	if logged_in():
		return render_template('create.html')

	return redirect("/")

@app.route('/viewDeck/<id>', methods=['GET'])
def viewDeck(id):
	cards = json.loads(
		decks.getDeckByID(id)[0][4]
		.replace("\'","\""))

	'''
	What's going on ^^^^

	Well, JSON doesn't recognize '', so we replace it before
	we load it.
	'''
	return render_template('viewDeck.html', deck=cards)



#######################################

'''
API stuff below
'''

@app.route("/download/<id>", methods=["GET"])
def toCSV(id):
	data = decks.getDeckByID(id)[0]
	cards = json.loads(data[4].replace("\'","\""))

	#^^^ if this is confusing see the docs on this func
	name = f'./CSV/{data[1]}_by_{data[2]}.csv'


	with open(name, "w") as f:
		writer = csv.writer(f,delimiter=",")
		writer.writerow(["question", "answer"])

		for pair in cards:
			writer.writerow([pair.get("question"), pair.get("answer")])

	return send_from_directory("./CSV", f'{data[1]}_by_{data[2]}.csv')



def removeImage(fPath):
		'''
		Removes image; utility for /render/
		'''
		try:
			os.remove(fPath)
		except:
			pass #tbd figure out what to do during exception


def renderImage(path):
		'''
		Renders image sent to it in queue. Will return no text if error.

		Schema
		error boolean : self explanatory
		error_message str : copy of error
		rendered_text str : string of results; returns None if error
		'''

		try:
			result = pytesseract.image_to_string(path)
			removeImage(path)
			return jsonify({
				"error":False,
				"error_message":None,
				"rendered_text":result
				})
		except TypeError as t:
			return jsonify({
				"error": True,
				"error_message":str(t),
				"rendered_text":None
				})
		except RuntimeError as r:
			return jsonify({
				"error": True,
				"error_message":str(r),
				"rendered_text":None
				})
		except Exception as e:
			return jsonify({
				"error": True,
				"error_message":str(e),
				"rendered_text":None
				})

#############
#API VVVV

@app.route("/render", methods=["POST"])
def render():
		'''
		Utility for adding Images for our queue.

		IF successful, will upload the image into the folder and queue the renderImage() function

		Elsewise will return error

		Schema:
		Error bool
		Error_message str
		Result str

		For more info see : https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/
		https://stackoverflow.com/questions/65483152/how-to-upload-file-to-flask-application-with-python-requests
		'''
		#checking if file has correct file path
		file = request.files.get("file")

		filename = secure_filename(file.filename)

		'''if filename.rsplit(".", 1)[1].lower() not in ALLOWED_EXTENSIONS:
			return jsonify({
				"error":True,
				"error_message":"File Type not Allowed",
				"result": None
				})'''

		if request.method == "POST":

			if 'file' not in request.files.keys() or file.filename == "":
				return render_template("create.html")

			else:
				filename = secure_filename(file.filename)
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				#uploading file ^^^
				#try:
				if True:
					'''result = renderImage(os.path.join(app.config['UPLOAD_FOLDER'], filename))
					paragraphed_text = json.loads(result.data)["rendered_text"].split("\n")
					

					questionPairs = () # tuple full of 

					for i in range(len(paragraphed_text)):
						if i > len(paragraphed_text):
							break

						elif i == len(paragraphed_text):
							questionPairs.append(
								{"question": paragraphed_text[i], 
								 "answer": "" 
								 }
								)
							break
						else:
							questionPairs.append({
								"question": paragraphed_text[i],
								"answer": paragraphed_text[i+1]
									}
								)
					'''
					questionPairs = ({"question": "question", "answer": "answer"},
									{"question": "question", "answer": "answer"},
									{"question": "question", "answer": "answer"},
									{"question": "question", "answer": "answer"})


					return render_template(
						"create_pt2.html",
						content = str(questionPairs)
						)

				'''except Exception as e:

					return render_template("create.html")'''
