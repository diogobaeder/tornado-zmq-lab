# Random reply times

This was a little experiment I've put together in some minutes while in TDC2011 (The Developers Conference), at São Paulo

It's just a silly almost-Hello-World, just to show the assynchronous communication working with non-blocking I/O through event
loops, mixed with a simple HTTP server

## Running
First, run some servers with different ports:

    $ ./server.py 8001 &

    $ ./server.py 8002 &

    $ ./server.py 8003 &

Then, run the client passing the ports you used for the servers as arguments:

    $ ./client.py 8001 8002 8003 &

Now, see how the random processing times from the services respond back to the client, asynchronously, and the client prints the
order in which it receives these replies in the HTTP response:

    $ curl http://127.0.0.1:8888