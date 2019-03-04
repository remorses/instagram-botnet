from .node import Node
from .schemas import user_schema
from modeller import Model




class User(Node, Model):
    _schema = user_schema
    __repr__ = lambda self: f'User(pk={self.pk}, username={self.username})'

    # id = property(lambda self: self['pk'])
