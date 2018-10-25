import tornado.web
import tornado.ioloop
import tornado.httpserver
from tornado.options import options, parse_command_line
import json
from client import http_post
parse_command_line()
tornado.options.define("port", default=8888, type=int)


class AppHandler(tornado.web.RequestHandler):
    def post(self):
        try:
            data = json.loads(self.request.body.decode('utf-8'))
            http_post(data)
        except Exception as e:
            print(e)
        # code = data["code"]


if __name__ == '__main__':
    app = tornado.web.Application([(r'/app/', AppHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.bind(tornado.options.options.port)
    http_server.start(0)
    tornado.ioloop.IOLoop.current().start()
