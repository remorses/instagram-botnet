from .node import Node



attributes = lambda x: (x._name, x._data)

class Hashtag(Node):
    __slots__ = ['_name', '_data']

    def __init__(self, *, generic=None, name=None, data=None):

        self._name = name
        self._data = data

        if generic:
            self._name = generic

    def __repr__(self):
        name, data = attributes(self)

        if name:
            return 'Hashtag(name=\'{}\')'.format(name)
        elif data:
            return 'Hashtag(data=\'{...}\')'

    @property
    def name(self):
        name, data = attributes(self)

        if name:
            return name
        else:
            return False
