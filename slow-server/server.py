#!/usr/bin/env python

import random
import sys
import time

import zmq
from zmq.eventloop import IOLoop

loop = IOLoop.instance()

context = zmq.Context()

rep = context.socket(zmq.REP)
rep.bind("tcp://127.0.0.1:5000")

def on_receive(sock, events):
    sock.recv()
    time.sleep(1)
    sock.send('0MQ response')

loop.add_handler(rep, on_receive, zmq.POLLIN)

loop.start()
