from .node import Node
from .common import attributes




class Arg(Node):

    def __init__(self, *, generic=None, value=None):
        self.value = value

        if generic:
            self.value = generic

    def __repr__(self):
            return 'Arg(value=\'{}\')'.format(self.value)
