from .sensors import RangeSensor, BinarySensor
from .displays import RangeDisplay, BinaryDisplay, RGBDisplay

SENSORS = {
    'light': RangeSensor('light', 0b00000000, 1 << 5),
    'button1': BinarySensor('button1', 0b11000010, 1 << 4),
    'button2': BinarySensor('button2', 0b11000100, 1 << 3),
    'knob': RangeSensor('knob', 0b01000000 , 1 << 2),
    'temperature': RangeSensor('temperature', 0b10000000, 1 << 1),
    'motion': BinarySensor('motion', 0b11000000, 1),
}

DISPLAYS = {
    'dashboard': RangeDisplay('dashboard', '000_____'),
    'led1': BinaryDisplay('led1', '001_____'),
    'led2': RGBDisplay('led2', '01______')
}
