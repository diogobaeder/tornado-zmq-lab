#!/usr/bin/env python

import sys
import time

import tornado
import tornado.web
import tornado.httpclient
#import zmq
#from zmq.eventloop import ioloop, zmqstream

#tornado.ioloop = ioloop


class ZmqHandler(tornado.web.RequestHandler):
    def __init__(self, *args, **kwargs):
        super(ZmqHandler, self).__init__(*args, **kwargs)

        self.counter = 0
        self.requests = 10
        self.stream = None

        self.create_stream()

    def create_stream(self):
        context = zmq.Context()
        req = context.socket(zmq.REQ)
        req.connect('tcp://127.0.0.1:5000')
        self.stream = zmqstream.ZMQStream(req, tornado.ioloop.IOLoop.instance())
        self.stream.on_recv(self.receive)

    def receive(self, message):
        self.write('got: %s' % message)
        self.finish()

    @tornado.web.asynchronous
    def get(self):
        print 'will send...'
        self.stream.send("")
        print 'sent.'


class HttpHandler(tornado.web.RequestHandler):
    def receive(self, response):
        self.write('got: %s' % response.body)
        self.finish()

    @tornado.web.asynchronous
    def get(self):
        http = tornado.httpclient.AsyncHTTPClient(max_clients=2000)
        http.fetch("http://localhost:8000/async-slow/", callback=self.receive)


class SlowHandler(tornado.web.RequestHandler):
    def get(self):
        time.sleep(1)
        self.write('HTTP response')


class AsyncSlowHandler(tornado.web.RequestHandler):
    def reply(self):
        self.write('HTTP response')
        self.finish()

    @tornado.web.asynchronous
    def get(self):
        tornado.ioloop.IOLoop.instance().add_timeout(time.time() + 1, self.reply)

application = tornado.web.Application([
    #(r'/zmq/', ZmqHandler),
    (r'/http/', HttpHandler),
    (r'/slow/', SlowHandler),
    (r'/async-slow/', AsyncSlowHandler),
])

port = sys.argv[1]
application.listen(port)

tornado.ioloop.IOLoop.instance().start()