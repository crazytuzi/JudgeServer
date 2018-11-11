import requests
import Judger


class Juder(object):
    languages = [
        'C++',
    ]
    extensions = [
        '.cpp',
    ]

    def __init__(self, data):
        self.data = data

    def writefile(self, name, content):
        with open('.cpp', 'w') as f:
            f.write('Hello, world!')

    def url(self):
        pass

    def response(self):
        url_tmp = self.url() + str(self.data["id"]) + "/"
        jdata = {
            "id": self.data["id"],
            "result": 5,
            "token": self.data["token"]
        }
        req = requests.put(url_tmp, json=jdata)
