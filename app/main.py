from flask import Flask, request, redirect, session, render_template, url_for
from database import Database
import json
from random import *
import os
import sqlite3

from database import UsernamePasswordTable, BlogTable #using database classes

myapp= flask(__name__)


db_file = "data.db"


userpass = UsernamePasswordTable(db_file, "userpass")
blog = BlogTable(db_file, "blog")
@myapp.route("/")
def homepage():
    return render_template("index.html")

@myapp.route("/", methods = ["POST"])
def checklogin():
    username = request.form["username"]
    password = request.form["password"]

       if (username=="" or password==""):
        return render_template('login.html', syntaxerror="Cannot submit blank username or password")
    elif not userpass.userExists(username):
        return render_template('login.html', syntaxerror="Username does not exist")
    elif not userpass.passMatch(username, password):
        return render_template('login.html', syntaxerror = "Incorrect password")
    else:
        session["username"] = username
        return redirect('/sloggedin')

@myapp.route("/loggedin")
def loggedin():
    return redirect("/index.html")

@myapp.route("/signup")
def signup():
    username= request.args['username']
    password= request.args['password']
    passauth= request.args['passauth']
        userpass.insert(username, password) # committing actions to database must be done every time you commit a command
        session["username"]=username
        return redirect("/loggedin")
    






if __name__ == "__main__":
    myapp.run()
