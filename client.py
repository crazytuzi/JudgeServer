import requests
url = "http://127.0.0.1:8000/api/submissiontoken/"


def http_post(data):
    url_tmp = url + str(data["id"]) + "/"
    jdata = {
        "id": data["id"],
        "result": 5,
        "token": data["token"]
    }
    req = requests.put(url_tmp, json=jdata)
