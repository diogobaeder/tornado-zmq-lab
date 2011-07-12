#!/usr/bin/env python

import random
import sys
import time

import zmq
from zmq.eventloop import IOLoop

loop = IOLoop.instance()

context = zmq.Context()

rep = context.socket(zmq.REP)
port = sys.argv[1]
rep.bind("tcp://127.0.0.1:%s" % port)

def on_receive(sock, events):
    sock.recv()
    time.sleep(random.randint(10, 100) / 1000.0)
    sock.send(port)

loop.add_handler(rep, on_receive, zmq.POLLIN)

loop.start()
