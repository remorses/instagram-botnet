from .node import Node




class Comment(Node):

    __slots__ = ['value']

    def __init__(self, *, generic=None, value=None):
        self.value = value

        if generic:
            self.value = generic

    def __repr__(self):
            return 'Comment(value=\'{}\')'.format(self.value)
