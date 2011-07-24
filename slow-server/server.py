#!/usr/bin/env python

import random
import sys
import time

import zmq
from zmq.eventloop import ioloop, zmqstream

loop = ioloop.IOLoop.instance()

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://127.0.0.1:5000")
stream = zmqstream.ZMQStream(socket, loop)

def on_receive(message):
    time.sleep(1)
    stream.send('0MQ response')

stream.on_recv(on_receive)

loop.start()
