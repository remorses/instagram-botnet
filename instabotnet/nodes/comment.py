from .node import Node
from modeller import Model
from .schemas import comment_schema
import traceback


class Comment(Node, Model):

    def _on_init(self):
        try:
            self._validate()
        except:
            print('ERROR in validation for Comment:')
            print()
            traceback.print_exc()
            print()
            print(self._yaml())
            print()

    _schema = comment_schema
