from .node import Node
from .common import attributes


def username_from_id(id):
    pass


class User(Node):

    def __init__(self, *, generic=None, id=None, username=None, data=None):
        self._username = username
        self._id = id
        self.data = data

        if generic:
            self._username = generic

    def __repr__(self):
        username, id, data = attributes(self)

        if username:
            return 'User(username=\'{}\')'.format(username)
        elif id:
            return 'User(id=\'{}\')'.format(id)
        elif data:
            return 'MediaUser(data=\'{...}\')'

    @property
    def username(self):
        username, id, data = attributes(self)

        if username:
            return username
        elif id:
            return username_from_id(id)
        elif data:
            return data['user']['username']
