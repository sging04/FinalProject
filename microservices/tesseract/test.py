from api import app

#other functions being tested not associated directly with app
from api import renderImage, removeImage

import pytest 
import json
import pytesseract
import os
import shutil #https://docs.python.org/3/library/shutil.html


from setup import TESSERACT_LOCATION


#https://flask.palletsprojects.com/en/2.1.x/testing/

#config stuff
pytesseract.pytesseract.tesseract_cmd = TESSERACT_LOCATION
##############


def test_Index():
	'''
	Tests Index Function of API
	See main.py for more info on that
	'''
	with app.test_client() as client:
		response = client.get("/api/")

		json_response = json.loads(response.data)
		#response.data returns bytes so things are a bit annoying
		assert json_response["error"] == False
		assert json_response["error_message"] is None
		print("All tests passed on test_Index()")

def test_renderImage_and_removeImage():
	'''
	Tests the renderImage() and removeImage() functions.

	I wouldn't tinker with this one. It has some dangerous behaviour and don't be that guy
	that does something to the folder structure....perhaps it's going to break too PLEASE

	tbh testing the actual endpoint for this might be a real pain because of it's behaviour so
	I'mma go on a limb and say that this will suffice
	'''
	with app.app_context():
		'''
		If you're not 100% sure what the above line is, don't worry about it
		But if you're really daring, then see the link below and go the section
		called "Manually Push a Context"
		'''

		folder = "./sampleImages"
		copy = "./sampleImagesCopy/sampleImages"

		shutil.copytree(folder, copy)

		for image in os.listdir(copy):

			'''
			Don't be that guy sticking nonImages into that folder
			It's going to break this function and the test because the test
			is done elsewhere
			'''
			json_response = json.loads(
				renderImage(os.path.join(copy, image)
					).data)

			assert json_response["error"] == False
			assert json_response["error_message"] is None
			assert not json_response["rendered_text"] is None
			print(f'Test for test_renderImage() passed with image from {os.path.join(copy, image)}')

		assert len(os.listdir(copy)) == 0
		print("Test for removeImage() passed!")
		shutil.rmtree(copy) #removing the temporary folder

def main():
	#test_Index()
	test_renderImage_and_removeImage()


if __name__ == '__main__':
	main()