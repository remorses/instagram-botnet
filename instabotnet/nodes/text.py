from .node import Node





class Text(Node):
    """
    a text message
    """

    __slots__ = ['value']

    def __init__(self, *, generic=None, value=None):
        self.value = value

        if generic:
            self.value = generic

    def __repr__(self):
            return 'Text(value=\'{}\')'.format(self.value)
