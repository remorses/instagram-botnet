from .node import Node




class Arg(Node):

    __slots__ = ['value']

    def __init__(self, *, generic=None, value=None):
        self.value = value

        if generic:
            self.value = generic

    def __repr__(self):
            return 'Arg(value=\'{}\')'.format(self.value)
