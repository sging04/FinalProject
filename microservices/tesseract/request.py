import requests as r


url = "http://127.0.0.1:8000/api/render"

files = {"file": (open("./sampleImages/test2.png", "rb"))}
headers = {
    "accept" : "application/json"
    }

response = r.request("POST", url, headers=headers, data={}, files=files)

print(response.text)
