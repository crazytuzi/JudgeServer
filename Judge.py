import requests
import os
import Judger
import Utlis
import time
from subprocess import PIPE, run


def output(command):
    result = run(
        command,
        stdout=PIPE,
        stderr=PIPE,
        universal_newlines=True,
        shell=True)
    return result.stdout


class Judge(object):
    languages = [
        [
            'C',
            '.c'
        ],
        [
            'C++',
            '.cpp'
        ],
        [
            'Python2',
            '.py'
        ],
        [
            'Python3',
            '.py'
        ],
        [
            'Java',
            '.java'
        ]
    ]
    file_extensions = [
        '.in',
        '.ans',
        '.out'
    ]

    def __init__(self, data):
        self.data = data
        self.problem_dir = Utlis.problem_dir(self.data['problem'])
        self.file_len = len([name for name in os.listdir(
            self.problem_dir) if os.path.isfile(os.path.join(self.problem_dir, name))])
        self.file_len //= 2
        # 都命名为Main，与Java统一
        self.timestamp = int(time.time())

        source_name = Utlis.answer_dir(
            self.data['id'], self.timestamp) + "Main" + self.languages[self.data['language']][1]
        output_name = Utlis.answer_dir(
            self.data['id'], self.timestamp) + "Main"
        if self.data['language'] == 4:
            output_name = output_name + ".class"
        os.mkdir(Utlis.answer_dir(self.data['id'], self.timestamp))
        self.writefile(source_name, self.data['code'])
        if self.data['language'] == 0:
            output("gcc %s -o %s" % (source_name, output_name))
        elif self.data['language'] == 1:
            output("g++ %s -o %s" % (source_name, output_name))
        elif self.data['language'] == 4:
            output("javac %s" % (source_name,))
        else:
            output_name = source_name
        if self.data['language'] == 4:
            source_name = Utlis.answer_dir(self.data['id'], self.timestamp)
        else:
            source_name = output_name

        self.RES = {}
        if os.path.exists(output_name):
            self.CFG = {
                'language': self.languages[self.data['language']][0],
                'source_name': source_name,
                'in_file': 'lll.in',
                'out_file': 'lll.out',
                'ans_file': 'lll.ans',
                'time_limit': self.data['time_cost'],
                'memory_limit': self.data['memory_cost'],
            }
            self.JudgeAll()
            self.response()
        else:
            self.RES['status'] = 8  # COMPILE_ERROR
            self.RES['use_time'] = 0
            self.RES['use_memory'] = 0
            self.response()

    def JudgeAll(self):
        max_use_time = -1
        max_use_memory = -1
        res = {}
        for i in range(self.file_len):
            in_file = self.problem_dir + str(i) + self.file_extensions[0]
            ans_file = self.problem_dir + str(i) + self.file_extensions[1]
            out_file = Utlis.answer_dir(
                self.data['id'],
                self.timestamp) + "Main" + '_' + str(i) + self.file_extensions[2]
            self.writefile(out_file)
            self.CFG['in_file'] = in_file
            self.CFG['out_file'] = out_file
            self.CFG['ans_file'] = ans_file
            res = self.JudgeOne(self.CFG)
            if res['status'] != 1:
                self.RES = res
                return
            elif res['use_time'] > max_use_time:
                max_use_time = res['use_time']
                max_use_memory = res['use_memory']
            elif res['use_time'] == max_use_time and res['use_memory'] > max_use_memory:
                max_use_memory = res['use_memory']
        res['use_time'] = max_use_time
        res['use_memory'] = max_use_memory
        self.RES = res

    def JudgeOne(self, config):
        res = Judger.run(config)
        return res

    def writefile(self, name, content=''):
        with open(name, 'w') as f:
            f.write(content)
            f.close()

    def response(self):
        url = Utlis.submission_url(self.data['id'])
        data = {
            "id": self.data['id'],
            "result": self.RES['status'],
            "time_cost": self.RES['use_time'],
            "memory_cost": self.RES['use_memory'],
            "token": self.data["token"]
        }
        requests.put(url, json=data)
