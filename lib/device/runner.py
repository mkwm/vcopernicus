from eventsource.client import EventSourceClient
import json
from socket import error as socket_error
import sys
from threading import Thread
from urllib2 import urlopen

from vcopernicus import DISPLAYS, SENSORS
from vcopernicus.settings import IOT_HYPERVISOR, IOT_NODENAME, IOT_SOCKET
from vcopernicus.utils import BitPattern

try:
    server_address = sys.argv[1]
except IndexError:
    print >>sys.stderr, 'Usage: %s serial_socket_path' % sys.argv[0]
    print >>sys.stderr, 'For example: %s /tmp/ttyS0.sock' % sys.argv[0]
    sys.exit(2)

try:
    IOT_SOCKET.connect(server_address)
except socket_error as msg:
    print >>sys.stderr, msg
    sys.exit(1)

def _esc_thread():
    def handler(event):
        if event.name == 'setup':
            for k, v in DISPLAYS.iteritems():
                urlopen('http://%s/devices/%s/sensors/%s' % (IOT_HYPERVISOR, IOT_NODENAME, k), data=v.internal_value)
        elif event.name in SENSORS:
            SENSORS[event.name].value = json.loads(event.data)
    esc = EventSourceClient(url=IOT_HYPERVISOR, action='devices/%s' % IOT_NODENAME, target='stream', callback=handler)
    esc.poll()

thread = Thread(target=_esc_thread)
thread.daemon = True
thread.start()

AUTOUPDATE = BitPattern('10______')
QUERY = BitPattern('11______')

def on_write(data):
    value = ord(data)
    if AUTOUPDATE & value:
        for sensor in SENSORS.itervalues():
            sensor.autoupdate = bool(sensor.query_bit & value)
    elif QUERY & value:
        for sensor in SENSORS.itervalues():
            if sensor.query_bit & value:
                IOT_SOCKET.send(chr(sensor.value))
    else:
        for display in DISPLAYS.itervalues():
            if not display.query_pattern & value: continue
            display.value = value
            break

while True:
    data = IOT_SOCKET.recv(1)
    on_write(data)
