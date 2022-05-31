from main import app
import pytest 

#https://flask.palletsprojects.com/en/2.1.x/testing/

@pytest.fixture()
def app():
	app = app
	app.config.update({"TESTING":True})


def test_Render(client):
	url = "/api/render/"

	payload = {}

	file = ('file', open("./tests/test1.png", "rb") ,'image/png')

	headers = {'accept': 'application/json'}

	#response = r.request("POST", url, headers=headers, data=payload, files=file)

	response = client.post("/api/render", files=file, headers=headers)
	print(response)
def main():
	test_Render()


if __name__ == '__main__':
	main()