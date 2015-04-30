from .sensors import RangeSensor, BinarySensor
from .displays import RangeDisplay, BinaryDisplay, RGBDisplay

_DEFAULT_SENSORS = {
    'light': (RangeSensor, (0b00000000, 1 << 5)),
    'button1': (BinarySensor, (0b11000010, 1 << 4)),
    'button2': (BinarySensor, (0b11000100, 1 << 3)),
    'knob': (RangeSensor, (0b01000000 , 1 << 2)),
    'temperature': (RangeSensor, (0b10000000, 1 << 1)),
    'motion': (BinarySensor, (0b11000000, 1)),
}

_DEFAULT_DISPLAYS = {
    'dashboard': (RangeDisplay, ('000_____', )),
    'led1': (BinaryDisplay, ('001_____', )),
    'led2': (RGBDisplay, ('01______', ))
}

def get_default_sensors(serial_write_func):
    result = {}
    for name, (SensorClass, args) in _DEFAULT_SENSORS.iteritems():
        result[name] = SensorClass(name, serial_write_func, *args)
    return result

def get_default_displays(display_show_func):
    result = {}
    for name, (DisplayClass, args) in _DEFAULT_DISPLAYS.iteritems():
        result[name] = DisplayClass(name, display_show_func, *args)
    return result
    