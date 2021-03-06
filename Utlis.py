import configparser
conf = configparser.ConfigParser()
conf.read("config.conf")
url = conf.items('url')
path = conf.items('path')


def problem_dir(problem):
    return path[0][1] + str(problem) + '/'


def answer_dir(problem, timestamp):
    return path[1][1] + str(timestamp) + "_" + str(problem) + '/'


def submission_url(submission):
    return url[0][1] + ':' + url[1][1] + \
        '/' + url[2][1] + str(submission) + '/'
