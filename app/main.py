from flask import Flask, request, redirect, session, render_template, url_for
import json
import os
import sqlite3
import requests as r
from database import UsernamePasswordTable, QuestionSetTable #using database classes


app= Flask(__name__)
app.secret_key = os.urandom(32)

db_file = "data.db"


userpass = UsernamePasswordTable(db_file, "userpass")
decks = QuestionSetTable(db_file, "decks")


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



@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "GET":
        return render_template("create.html" )

    elif request.method == "POST":
        files = request.files.getlist("files")

        text = ""

        for file in files:
            url = "/api/render"

            files = {"file": (open(file, "rb"))}
            headers = {
                "accept" : "application/json"
            }

            response = r.request("POST", url, headers=headers, data={}, files=file)

            if not response["error"]:
                text += response["result"]

        return render_template("edit.html", text=text)

@app.route("/viewDeck/<id>", methods=["GET"])
def viewDeck(id):
    return render_template(
        "viewDeck.html",
        data=decks.getDeckByID(id))



app.secret_key = "secret key"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Get current path
path = os.getcwd()
# file Upload
UPLOAD_FOLDER = os.path.join(path, 'uploads')

# Make directory if uploads is not exists
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed extension you can set your own
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/upload', methods=['POST'])
def upload_form():
    return render_template('upload.html')
def upload_file():
    if request.method == 'POST':

        if 'files[]' not in request.files:
            flash('No file part')
            return redirect(request.url)

        files = request.files.getlist('files[]')

        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        flash('File(s) successfully uploaded')
        return redirect('/viewDeck')
