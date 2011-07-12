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
        self.streams = []

        self.setup_sockets()

    def setup_sockets(self):
        context = zmq.Context()

        ports = sys.argv[1:]
        for port in ports:
            self.create_streams(context, port)

    def create_streams(self, context, port):
        req = context.socket(zmq.REQ)
        req.connect('tcp://127.0.0.1:%s' % port)
        stream = zmqstream.ZMQStream(req, tornado.ioloop.IOLoop.instance())
        stream.on_recv(self.receive)
        self.streams.append(stream)

    def receive(self, port):
        self.write('response from %s\n' % port)
        self.counter += 1
        if self.received_all_responses():
            self.finish()

    def received_all_responses(self):
        return self.counter == (len(self.streams) * self.requests)

    @tornado.web.asynchronous
    def get(self):
        for i in range(10):
            for stream in self.streams:
                stream.send("")

application = tornado.web.Application([(r'/', Handler)])

application.listen(8888)

tornado.ioloop.IOLoop.instance().start()