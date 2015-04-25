from .settings import IOT_SOCKET


class Sensor(object):
    def __init__(self, name, response_base, query_bit):
        self.name = name
        self.response_base = response_base
        self._internal_value = None
        self.autoupdate = False
        self.query_bit = query_bit
    
    @property
    def internal_value(self):
        return self.response_base + self._internal_value
    
    @internal_value.setter
    def internal_value(self, value):
        self._internal_value = value
        if self.autoupdate:
            IOT_SOCKET.send(chr(self.internal_value))
    
    @property
    def value(self):
        return self.internal_value


class BinarySensor(Sensor):
    @Sensor.value.setter
    def value(self, value):
        self.internal_value = int(value)


class RangeSensor(Sensor):
    @Sensor.value.setter
    def value(self, value):
        self.internal_value = int(value / 100. * 63)
