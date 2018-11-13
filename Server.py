import tornado.web
import tornado.ioloop
import tornado.httpserver
from tornado.options import options, parse_command_line
import json
from multiprocessing import Manager, Pool, cpu_count
from Producer import Producer
from Customer import Customer
parse_command_line()
tornado.options.define("port", default=8888, type=int)


def producer(q, data):
    Producer.producer(q, data)


def customer(q):
    Customer.customer(q)


# 队列
Q = Manager().Queue()
# 线程池
process = Pool(processes=cpu_count())
for i in range(cpu_count()):
    process.apply_async(customer, args=(Q,))


class AppHandler(tornado.web.RequestHandler):
    def post(self):
        try:
            data = json.loads(self.request.body.decode('utf-8'))
            producer(Q, data)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    app = tornado.web.Application([(r'/app/', AppHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.bind(tornado.options.options.port)
    http_server.start(0)
    tornado.ioloop.IOLoop.current().start()
    process.close()
    process.join()
