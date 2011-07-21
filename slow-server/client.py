#!/usr/bin/env python

import sys

import tornado
import tornado.web
import zmq
from zmq.eventloop import ioloop, zmqstream

tornado.ioloop = ioloop


class Handler(tornado.web.RequestHandler):
    def __init__(self, *args, **kwargs):
        super(Handler, self).__init__(*args, **kwargs)

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
        self.stream.send("")

application = tornado.web.Application([(r'/', Handler)])

port = sys.argv[1]
application.listen(port)

tornado.ioloop.IOLoop.instance().start()