from gevent import monkey; monkey.patch_all()
from gevent import spawn
from gevent.wsgi import WSGIServer
from gevent.queue import Queue

from flask import Flask, Response, request, render_template

from collections import defaultdict
import os
import time


class ServerSentEvent(object):
    def __init__(self, event, data):
        self.data = data
        self.event = event
        self.id = None
        self.desc_map = {self.data: 'data', self.event : 'event', self.id : 'id'}

    def encode(self):
        if not self.data:
            return ''
        lines = ['%s: %s' % (v, k) for k, v in self.desc_map.iteritems() if k]
        return '%s\n\n' % '\n'.join(lines)


app = Flask(__name__)
subscriptions = defaultdict(list)

@app.route('/')
def index():
    return render_template('index.html', devices=subscriptions)

@app.route('/devices/<device>/')
def device(device):
    return render_template('device.html', device=device)

@app.route('/devices/<device>/sensors')
def publish(device):
    data = ('setup', '')
    def notify():
        for sub in subscriptions[device][:]:
            sub.put(data)
    spawn(notify)
    return 'OK'

@app.route('/devices/<device>/sensors/<sensor>', methods=['POST'])
def setup(device, sensor):
    data = (sensor, request.get_data())
    def notify():
        for sub in subscriptions[device][:]:
            sub.put(data)
    spawn(notify)
    return 'OK'

@app.route('/devices/<device>/stream')
def stream(device):
    def gen():
        q = Queue()
        subscriptions[device].append(q)
        try:
            while True:
                event, data = q.get()
                ev = ServerSentEvent(event, data)
                yield ev.encode()
        except GeneratorExit:
            subscriptions[device].remove(q)
    return Response(gen(), mimetype='text/event-stream')

def run_entry_point():
    app.debug = True
    server = WSGIServer(('', 8080), app)
    server.serve_forever()
