import re


class BitPattern:
    def __init__(self, mask):
        if mask:
            if len(mask) != 8 or not re.match('^[01]*_+$', mask):
                raise ValueError('`{0}` is not a valid 8-bit mask'.format(mask))
            self._low = int(mask.replace('_', '0'), 2)
            self._high = int(mask.replace('_', '1'), 2)
        else:
            self._low = -1
            self._high = -1

    def __and__(self, value):
        return self._low <= value <= self._high
