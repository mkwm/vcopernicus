from collections import OrderedDict

commands = OrderedDict()


class Registry(object):
    def __call__(self):
        def decorator(cls):
            commands[cls.__name__] = cls
            return cls
        return decorator


register = Registry()
