from .node import Node
from modeller import Model
from .schemas import comment_schema



class Comment(Node, Model):
    _schema = comment_schema
