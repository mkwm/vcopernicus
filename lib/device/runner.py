from eventsource.client import EventSourceClient
import json
import sys
from threading import Thread
from urllib2 import urlopen

from vcopernicus import get_default_displays, get_default_sensors
from vcopernicus.utils import BitPattern

import os
from socket import gethostname, socket, AF_UNIX, SOCK_STREAM

IOT_HYPERVISOR = os.environ.get('IOT_HYPERVISOR', 'localhost:8080')
IOT_NODENAME = os.environ.get('IOT_NODENAME', gethostname())


AUTOUPDATE = BitPattern('10______')
QUERY = BitPattern('11______')


class CopernicusImpl(object):
    def __init__(self, hypervisor, nodename, path):
        self._pattern = 'http://%s/devices/%s/sensors/%%s' % (hypervisor, nodename)
        self.esc = EventSourceClient(url=hypervisor, action='devices/%s' % nodename, target='stream', callback=self._esc_handler)
        self.thread = Thread(target=lambda: self.esc.poll())
        self.thread.daemon = True
        self.handlers = []
        self.socket = socket(AF_UNIX, SOCK_STREAM)
        self.socket.connect(path)

    def run(self):
        self.thread.start()

    def _esc_handler(self, event):
        data = json.loads(event.data)
        for handler in self.handlers:
            handler(event.name, data)
    
    def serial_read(self):
        return ord(self.socket.recv(1))
    
    def serial_write(self, data):
        self.socket.send(chr(data))
    
    def display_show(self, name, data):
        urlopen(self._pattern % name, data=json.dumps(data))


class VCopernicusServer(object):
    def __init__(self, client):
        self.client = client
        self.client.handlers.append(self.handle_input)
        self.displays = get_default_displays(self.client.display_show)
        self.sensors = get_default_sensors(self.client.serial_write)
    
    def handle_input(self, name, value):
        if name == 'setup':
            for display in self.displays.itervalues():
                display.flush()
        elif name in self.sensors:
            self.sensors[name].value = value
    
    def handle_serial(self):
        value = self.client.serial_read()
        if AUTOUPDATE & value:
            for sensor in self.sensors.itervalues():
                sensor.autoupdate = bool(sensor.query_bit & value)
        elif QUERY & value:
            for sensor in self.sensors.itervalues():
                if sensor.query_bit & value:
                    sensor.flush()
        else:
            for display in self.displays.itervalues():
                if not display.query_pattern & value: continue
                display.value = value
    
    def run_forever(self):
        self.client.run()
        while True:
            self.handle_serial()

def run():
    client = CopernicusImpl(IOT_HYPERVISOR, IOT_NODENAME, sys.argv[1])
    server = VCopernicusServer(client)
    server.run_forever()

if __name__ == '__main__':
    run()