import requests
import os
import Judger
import Utlis


class Judge(object):
    languages = [
        'C++',
    ]
    extensions = [
        '.cpp',
    ]
    file_extensions = [
        '.in',
        '.ans',
        '.out'
    ]

    def __init__(self, data):
        self.data = data
        self.problem_dir = Utlis.problem_dir(data['problem'])
        self.file_len = len([name for name in os.listdir(
            self.problem_dir) if os.path.isfile(os.path.join(self.problem_dir, name))])
        self.file_len //= 2
        source_name = Utlis.answer_dir(
        ) + str(self.data['id']) + self.extensions[0]
        self.writefile(source_name, self.data['code'])
        self.CFG = {
            'language': self.languages[0],
            'source_name': source_name,
            'in_file': 'lll.in',
            'out_file': 'lll.out',
            'ans_file': 'lll.ans',
            'time_limit': self.data['time_cost'],
            'memory_limit': self.data['memory_cost'],
            'compile option': ['-O2', '-lm', '-DONLINE_JUDGE']
        }
        self.JudgeAll()

    def JudgeAll(self):
        for i in range(self.file_len):
            in_file = self.problem_dir + str(i) + self.file_extensions[0]
            ans_file = self.problem_dir + str(i) + self.file_extensions[1]
            out_file = Utlis.answer_dir(
            ) + str(self.data['id']) + '_' + str(i) + self.file_extensions[2]
            self.writefile(out_file)
            self.CFG['in_file'] = in_file
            self.CFG['out_file'] = out_file
            self.CFG['ans_file'] = ans_file
            RES = self.JudgeOne(self.CFG)
            print(RES)

    def JudgeOne(self, config):
        RES = Judger.run(config)
        return RES

    def writefile(self, name, content=''):
        with open(name, 'w') as f:
            f.write(content)
            f.close()

    def response(self):
        url_tmp = self.url() + str(self.data["id"]) + "/"
        jdata = {
            "id": self.data["id"],
            "result": 5,
            "token": self.data["token"]
        }
        req = requests.put(url_tmp, json=jdata)
