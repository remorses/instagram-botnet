from .node import Node
from modeller import Model



class Arg(Node, Model):
    _schema = {'value': {'type': 'string'}}
