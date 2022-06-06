import os


TESSERACT_LOCATION = ""
UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")

with open("location.txt", "r") as f:
	TESSERACT_LOCATION = f.readlines()[1]


