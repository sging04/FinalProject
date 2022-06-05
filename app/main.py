from flask import Flask, request, redirect, session, render_template, url_for
import json
import os
import sqlite3

from database import UsernamePasswordTable #using database classes

app= Flask(__name__)
app.secret_key = os.urandom(32)

db_file = "data.db"


userpass = UsernamePasswordTable(db_file, "userpass")


@app.route("/",  methods=["GET"])
def disp_loginpage():
    if (not session.get("username") is None):
        # if
        # if there's an existing session, shows welcome page
        if request.method == "GET":
            # if there's an existing session, shows welcome page
            return redirect("/home")

    if ("username" != None):
        return render_template( 'login.html' )


@app.route("/signup", methods=["POST","GET"])
def signup():
    if session['username'] is not none:
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

@app.route("/create", methods=["GET"])
def create():
    # if session['username'] is not none:
    #     redirect("/")
    # for form in formFileMultiple:
    #     form= request.args["file"]
    return render_template("create.html" )


@app.route("/home", methods=["GET"])
def home():
    return render_template(
        "home.html",
        username=session.get("username"),
        decks = [1,2,3,3]
        )
