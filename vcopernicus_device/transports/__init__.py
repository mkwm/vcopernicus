from eventsource.client import EventSourceClient
import json
from threading import Thread
from urllib2 import urlopen


class VCopernicusTransportBase(object):
    def __init__(self, args):
        self._pattern = 'http://%s/devices/%s/sensors/%%s' % (args.coordinator, args.name)
        self.esc = EventSourceClient(url=args.coordinator, action='devices/%s' % args.name, target='stream', callback=self._esc_handler)
        self.thread = Thread(target=lambda: self.esc.poll())
        self.thread.daemon = True
        self.handlers = []

    def run(self):
        self.thread.start()

    def _esc_handler(self, event):
        data = json.loads(event.data)
        for handler in self.handlers:
            handler(event.name, data)
    
    def display_show(self, name, data):
        urlopen(self._pattern % name, data=json.dumps(data))
    
    @staticmethod
    def parse_args(args):
        pass