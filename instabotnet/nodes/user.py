from .node import Node
from .schemas import user_schema
from modeller import Model
import traceback



class User(Model, Node):
    def _on_init(self):
        try:
            self._validate()
        except Exception as e:
            print('ERROR in validation for User:')
            print()
            print(str(e))
            print()
            print(self._yaml())
            print()
            
    _schema = user_schema
    __repr__ = lambda self: f'User(pk={self.pk}, username={self.username})'

    # id = property(lambda self: self['pk'])
