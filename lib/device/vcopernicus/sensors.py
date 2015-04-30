class Sensor(object):
    def __init__(self, name, serial_write_func, response_base, query_bit):
        self._serial_write_func = serial_write_func
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
            self.flush()
    
    @property
    def value(self):
        raise AttributeError('value is write-only property; use internal_value instead')
    
    def flush(self):
        self._serial_write_func(self.internal_value)


class BinarySensor(Sensor):
    @Sensor.value.setter
    def value(self, value):
        self.internal_value = int(value)


class RangeSensor(Sensor):
    @Sensor.value.setter
    def value(self, value):
        self.internal_value = int(value / 100. * 63)
