from .node import Node
from modeller import Model



attributes = lambda x: (x._name, x._data)

class Hashtag(Model, Node):
    _schema = {
        'properties':
            {
                'name': {'type': 'string'}
            },
        'type': 'object',
    }
