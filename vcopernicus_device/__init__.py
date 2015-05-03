import argparse
import os
from socket import gethostname, socket, AF_UNIX, SOCK_STREAM
import sys

from .sensors import get_default_sensors
from .displays import get_default_displays
from .utils import BitPattern, transports as TRANSPORTS
from .transports import fd, pty, unix


AUTOUPDATE = BitPattern('10______')
QUERY = BitPattern('11______')


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
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--coordinator', help='set coordinator location',
                        default=os.environ.get('IOT_HYPERVISOR', 'localhost:8080'))
    parser.add_argument('-n', '--name', help='set node name',
                        default=os.environ.get('IOT_NODENAME', gethostname()))
    subparsers = parser.add_subparsers(help='transport type', dest='transport')
    for name, transport in TRANSPORTS.iteritems():
        s = subparsers.add_parser(name)
        transport.parse_args(s)
    args = parser.parse_args()
    print args
    client = transports[args.transport](args)
    server = VCopernicusServer(client)
    server.run_forever()