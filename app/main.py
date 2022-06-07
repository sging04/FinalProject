from flask import Flask, request, redirect, session, render_template, url_for, jsonify
import json
import os
import sqlite3
import requests as r
from database import UsernamePasswordTable, QuestionSetTable #using database classes

#misc imports
import pytesseract
from werkzeug.utils import secure_filename
import os
import json

#######################
#api stuff


from setup import TESSERACT_LOCATION, UPLOAD_FOLDER

#--------
# config stuffs dont touch!

app= Flask(__name__)
app.secret_key = os.urandom(32)

db_file = "data.db"

pytesseract.pytesseract.tesseract_cmd = TESSERACT_LOCATION
#might make a config file for this ^^^ will update
ALLOWED_EXTENSIONS = ["png", "jpg", "jpeg"]
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


userpass = UsernamePasswordTable(db_file, "userpass")
decks = QuestionSetTable(db_file, "decks")
#---------

def logged_in():
    """Returns logged in or not."""
    print(session.keys())
    return 'username' in session.keys()


@app.route("/",  methods=["GET"])
def disp_loginpage():
<<<<<<< HEAD
    if (not session.get("username") is None):
    	return render_template("home.html")
    else:
=======
    if loggedin():
        # if
        # if there's an existing session, shows welcome page
        if request.method == "GET":
            # if there's an existing session, shows welcome page
            return redirect("/home")

    if ("username" != None):
>>>>>>> fe8eb8715346cd5316d39cdabf8e56f521fb665b
        return render_template( 'login.html' )


@app.route("/signup", methods=["GET", "POST"])
def signup():
<<<<<<< HEAD
    if session.get("username") is not None:
=======
    if "username" in session:
        return redirect("/")

    if request.method == "GET":
        return render_template("signup.html")
    if request.method == "POST":
            username = request.form.get("name", default="")
            password = request.form.get("password", default="")
            password2 = request.form.get("password2", default="")



    if session['username'] is not none:
>>>>>>> fe8eb8715346cd5316d39cdabf8e56f521fb665b
        redirect("/")
    if request.method == "GET":
        return render_template("signup.html")
    elif request.method == "POST":
        username= request.args['username']
        password= request.args['password']
        passauth= request.args['passauth']
        userpass.insert(username, password) # committing actions to database must be done every time you commit a command
        session["username"]=username
        return redirect("/home", username=session.get("username"))


@app.route("/home", methods=["GET"])
def home():

    return render_template(
        "home.html",
        username=session.get("username"),
        decks = decks.getRandomEntries(10)
        )

@app.route("/logout")
def logout():
    #if "username" in session:
    session["username"] = None
    session.pop("username", None)
    return redirect('/')



@app.route("/create", methods=["GET"])
def create():
    return render_template("create.html" )


@app.route("/viewDeck/<id>", methods=["GET"])
def viewDeck(id):
    return render_template(
        "viewDeck.html",
        data=decks.getDeckByID(id))

'''
@app.route('/upload', methods=['GET'])
def upload_form():
    return render_template('upload.html')
'''
#######################################

'''
API stuff below
'''


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
			result = pytesseract.image_to_string(path, timeout=5)
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
				try:
					result = renderImage(os.path.join(app.config['UPLOAD_FOLDER'], filename))
					return render_template(
						"create_pt2.html",
						content = json.loads(result.data)["rendered_text"]
						)

				except Exception as e:
					return render_template("create.html")
