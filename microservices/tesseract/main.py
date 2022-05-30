from flask import Flask, jsonify


#--------
# config stuffs dont touch!

app = Flask(__name__)

#---------


@app.route("/")
def index():
	try:
		return jsonify({"error":False})

	except:	
		return jsonify({"error":True,})