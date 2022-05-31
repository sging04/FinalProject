from flask import Flask, request, redirect, session, render_template, url_for
import json
from random import *
import os
import sqlite3

from database import UsernamePasswordTable #using database classes

app= Flask(__name__)
app.secret_key = os.urandom(32)


db_file = "data.db"


userpass = UsernamePasswordTable(db_file, "userpass")
@app.route("/",  methods=["GET", "POST"])
def disp_loginpage():
    if (session.get("username") is not None):
        # if there's an existing session, shows welcome page
        if request.method == "GET":
            # if there's an existing session, shows welcome page
            return render_template( 'response.html', username=session.get("username") )
        else:
            topic = request.form['topic']
            data = blog.seeContent()
            return render_template( 'response.html', username=session.get("username"), topic=topic, data=data )
    if ("username" != None):
        return render_template( 'login.html' )



@app.route("/loggedin")
def loggedin():
    return redirect("/")

@app.route("/signup", methods=["POST","GET"])
def signup():
    if session['username'] is not none:
        redirect("loggedin")
    if request.method == "GET":
        return render_template("signup.html")
    elif request.method == "POST":
        username= request.args['username']
        password= request.args['password']
        passauth= request.args['passauth']
        userpass.insert(username, password) # committing actions to database must be done every time you commit a command
        session["username"]=username
        return redirect("/loggedin")
    






if __name__ == "__main__":
    app.run(debug=True)

