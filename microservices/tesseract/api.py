
from flask import Flask, jsonify, request
#queue stuff tbd


#misc imports
import pytesseract
from werkzeug.utils import secure_filename
import os
import json

from setup import TESSERACT_LOCATION, UPLOAD_FOLDER

#--------
# config stuffs dont touch!

app = Flask(__name__)

pytesseract.pytesseract.tesseract_cmd = "/usr/local/Cellar/tesseract/5.1.0/bin/tesseract"
#might make a config file for this ^^^ will update
UPLOAD_FOLDER = "/Users/user/Desktop/Final Proj/FinalProject/microservices/tesseract/uploads"
ALLOWED_EXTENSIONS = ["png", "jpg", "jpeg"]
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#---------

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
	except:
		return jsonify({
			"error": True,
			"error_message":"Unknown Error, check logs",
			"rendered_text":None
			})

@app.route("/api", methods=['GET'])
def index():
	'''
	Testing if server is alive; don't use in production

	Schema
	error boolean : returns true if no errors; elsewise false
	error_message str: returns an error message if error is true, elsewise is None
	'''
	try:
		return jsonify({
			"error":False,
			"error_message":None
			})

	except Exception as e:	
		return jsonify({
			"error":True,
			"error_message":str(e)})



@app.route("/api/render", methods=["POST"])
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

	filename = secure_filename(request.files['file'].filename)

	if filename.rsplit(".", 1)[1].lower() not in ALLOWED_EXTENSIONS:
		return jsonify({
			"error":True,
			"error_message":"File Type not Allowed",
			"result": None
			})
	if request.method == "POST":

		if 'file' not in request.files.keys():
			return jsonify({
				"error":True,
				"error_message": "Upload not Found!",
				"result": None
				})
		file = request.files['file']

		if file.filename == "":
			return jsonify({
				"error":True,
				"error_message": "No Selected File",
				"result":None
				})
		else:
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			#uploading file ^^^
			try:
				result = renderImage(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				return jsonify({
	            	"error":False,
	            	"error_message": None,
	            	"result": json.loads(result.data)["rendered_text"]
	            	})
			except Exception as e:
				return jsonify({"error":True,
	            	"error_message": str(e),
	            	"result":None
	            	})




