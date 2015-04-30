from .utils import BitPattern


class Display(object):
    def __init__(self, name, display_show_func, query_pattern=None):
        self._display_show_func = display_show_func
        self.name = name
        self.query_pattern = BitPattern(query_pattern)
        self._internal_value = None
    
    @property
    def internal_value(self):
        return self._internal_value
    
    @internal_value.setter
    def internal_value(self, value):
        self._internal_value = value
        self.show()
    
    @property
    def value(self):
        raise AttributeError('value is write-only property; use internal_value instead')
    
    def show(self):
        self._display_show_func(self.name, self.internal_value)


class RangeDisplay(Display):
    @Display.value.setter
    def value(self, value):
        self.internal_value = int((value & 0b00011111) / 31. * 100)


class BinaryDisplay(Display):
    @Display.value.setter
    def value(self, value):
        self.internal_value = bool(value & 0b00000001)


class RGBDisplay(Display):
    @Display.value.setter
    def value(self, value):
        value = value & 0b00111111
        COLOR_STEP = 0xff / 3
        color = sum([(value & (0b11 << i*2)) / (1 << i*2) * (1 << i*8) for i in xrange(3)]) * COLOR_STEP
        self.internal_value = '{0:06x}'.format(color)


_DEFAULT_DISPLAYS = {
    'dashboard': (RangeDisplay, ('000_____', )),
    'led1': (BinaryDisplay, ('001_____', )),
    'led2': (RGBDisplay, ('01______', ))
}


def get_default_displays(display_show_func):
    result = {}
    for name, (DisplayClass, args) in _DEFAULT_DISPLAYS.iteritems():
        result[name] = DisplayClass(name, display_show_func, *args)
    return result