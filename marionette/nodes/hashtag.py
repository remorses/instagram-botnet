from .node import Node
from .common import attributes





class Hashtag(Node):

    def __init__(self, *, generic=None, name=None, id=None, data=None):

        self._name = name
        self._id = id
        self._data = data

        if generic:
            self._name = generic

    def __repr__(self):
        name, id, data = attributes(self)

        if name:
            return 'Hashtag(name=\'{}\')'.format(name)
        elif id:
            return 'Hashtag(id=\'{}\')'.format(id)
        elif data:
            return 'Hashtag(data=\'{...}\')'

    @property
    def name(self):
        name, id, data = attributes(self)

        if name:
            return name
        # elif id:
        #     return name_from_id(id)
        elif data:
            return data['user']['name']
        else:
            return False

    # @property
    # def id(self):
    #     name, id, data = attributes(self)
    #     if id:
    #         return id
    #     elif data:
    #         return data['user']['name']
    #     else:
    #         return False
