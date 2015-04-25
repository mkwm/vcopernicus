from urllib2 import urlopen

from .utils import BitPattern
from .settings import IOT_HYPERVISOR, IOT_NODENAME


class Display(object):
    def __init__(self, name, query_pattern=None):
        self.name = name
        self.query_pattern = BitPattern(query_pattern)
        self._internal_value = None
    
    @property
    def internal_value(self):
        return self._internal_value
    
    @internal_value.setter
    def internal_value(self, value):
        self._internal_value = value
        urlopen('http://%s/devices/%s/sensors/%s' % (IOT_HYPERVISOR, IOT_NODENAME, self.name), data=self._internal_value)
    
    @property
    def value(self):
        return self.internal_value


class RangeDisplay(Display):
    @Display.value.setter
    def value(self, value):
        self.internal_value = str(int((value & 0b00011111) / 31. * 100))


class BinaryDisplay(Display):
    @Display.value.setter
    def value(self, value):
        self.internal_value = 'true' if (value & 0b00000001) else 'false'


class RGBDisplay(Display):
    @Display.value.setter
    def value(self, value):
        value = value & 0b00111111
        COLOR_STEP = 0xff / 3
        color = sum([(value & (0b11 << i*2)) / (1 << i*2) * (1 << i*8) for i in xrange(3)]) * COLOR_STEP
        self.internal_value = '"{0:06x}"'.format(color)
