from .node import Node
from modeller import Model



attributes = lambda x: (x._name, x._data)

class Hashtag(Node, Model):
    _schema = {
        'properties':
            {
                'name': {'type': 'string'}
            },
        'type': 'object',
    }
