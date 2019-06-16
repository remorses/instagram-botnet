from .node import Node
from modeller import Model



class Arg(Model, Node):
    _schema = {
        'properties':
            {
                'value': {'type': 'string'}
            },
        'type': 'object',
    }
