from .node import Node
from modeller import Model
from .schemas import comment_schema
import traceback


class Comment(Model, Node):

    def _on_init(self):
        try:
            self._validate()
        except Exception as e:
            print('ERROR in validation for Comment:')
            print()
            print(str(e))
            print()
            print(self._yaml())
            print()

    _schema = comment_schema
