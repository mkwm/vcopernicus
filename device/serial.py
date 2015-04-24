from collections import defaultdict
from eventsource.client import EventSourceClient
import json
import os
from socket import gethostname
from time import sleep
from threading import Thread
from urllib2 import urlopen
from Queue import Queue


IOT_HYPERVISOR = os.environ.get('IOT_HYPERVISOR', 'hypervisor.iot:5000')


class Serial(object):
    def _esc_thread(self):
        def handler(event):
            if event.name in ('button1', 'button2', 'motion'):
                self.state[event.name] = 1 if json.loads(event.data) else 0
                if self.autoupdate[event.name]:
                    self.queue.put(self.mod[event.name] + self.state[event.name])
            elif event.name in ('knob', 'light', 'temperature'):
                self.state[event.name] = int(json.loads(event.data) / 100. * 63)
                if self.autoupdate[event.name]:
                    self.queue.put(self.mod[event.name] + self.state[event.name])
            elif event.name in ('led1', 'led2', 'dashboard'):
                self.display[event.name] = event.data
            elif event.name == 'setup':
                for k, v in self.display.iteritems():
                    urlopen('http://%s/%s/publish?event=%s&data=%s' % (IOT_HYPERVISOR, self.device, k, v))
        esc = EventSourceClient(url=IOT_HYPERVISOR, action=self.device, target='subscribe', callback=handler)
        esc.poll()

    def __init__(self, *args, **kwargs):
        self.device = os.environ.get('IOT_NODENAME', gethostname())
        self.thread = Thread(target=self._esc_thread)
        self.thread.daemon = True
        self.thread.start()
        self.queue = Queue()
        self.state = dict(knob=0, button1=0, button2=0, light=0, motion=0, temperature=24)
        self.display = dict(led1='false', led2='false', dashboard='0')
        self.autoupdate = defaultdict(lambda: False)
        self.mod = dict(knob=0b01000000, button1=0b11000010, button2=0b11000100, light=0b00000000,
                        motion=0b11000000, temperature=0b10000000)

    def read(self, size=1):
        result = ''
        for _ in xrange(size):
            result += chr(self.queue.get())
        return result

    def write(self, data):
        value = ord(data)
        if (value & ~0b00011111) == 0b00000000:
            event = 'dashboard'
            data = int((value & ~0b11100000) / 31. * 100)
            urlopen('http://%s/%s/publish?event=%s&data=%s' % (IOT_HYPERVISOR, self.device, event, data))
        elif (value & ~0b00011111) == 0b00100000:
            event = 'led1'
            data = 'true' if (value & 0b00000001) == 0b00000001 else 'false'
            urlopen('http://%s/%s/publish?event=%s&data=%s' % (IOT_HYPERVISOR, self.device, event, data))
        elif (value & ~0b00111111) == 0b01000000:
            event = 'led2'
            color = ['00', '00', '00']
            r = value & 0b00110000
            if r == 0b00110000: color[0] = 'FF'
            elif r == 0b00100000: color[0] = 'AA'
            elif r == 0b00010000: color[0] = '55'
            g = value & 0b00001100
            if g == 0b00001100: color[1] = 'FF'
            elif g == 0b00001000: color[1] = 'AA'
            elif g == 0b00000100: color[1] = '55'
            b = value & 0b00000011
            if b == 0b00000011: color[2] = 'FF'
            elif b == 0b00000010: color[2] = 'AA'
            elif b == 0b00000001: color[2] = '55'
            data = '"%s"' % ''.join(color)
            urlopen('http://%s/%s/publish?event=%s&data=%s' % (IOT_HYPERVISOR, self.device, event, data))
        elif (value & ~0b00111111) == 0b10000000:
            self.autoupdate['light'] = bool(value & 0b00100000)
            self.autoupdate['button1'] = bool(value & 0b00010000)
            self.autoupdate['button2'] = bool(value & 0b00001000)
            self.autoupdate['knob'] = bool(value & 0b00000100)
            self.autoupdate['temperature'] = bool(value & 0b00000010)
            self.autoupdate['motion'] = bool(value & 0b00000001)
        elif (value & ~0b00111111) == 0b11000000:
            if value & 0b00100000: self.queue.put(self.mod['light'] + self.state['light'])
            if value & 0b00010000: self.queue.put(self.mod['button1'] + self.state['button1'])
            if value & 0b00001000: self.queue.put(self.mod['button2'] + self.state['button2'])
            if value & 0b00000100: self.queue.put(self.mod['knob'] + self.state['knob'])
            if value & 0b00000010: self.queue.put(self.mod['temperature'] + self.state['temperature'])
            if value & 0b00000001: self.queue.put(self.mod['motion'] + self.state['motion'])

    def flush(self):
        pass
