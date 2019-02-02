from collections import OrderedDict
from types import FunctionType


# returns the attributes of the class,
# TODO, in pyton 3.2 attribtes aren't ordered
def attributes(instance):
    list = [
        v
        for k, v in instance.__dict__.items()
        if not k.startswith('__') and not k.endswith('__')
        and not isinstance(v, (FunctionType, classmethod, staticmethod))
        ]
    return tuple(list)
