from .node import Node
from modeller import Model



class Arg(Node, Model):
    _schema = {
        'properties':
            {
                'value': {'type': 'string'}
            },
        'type': 'object',
    }
