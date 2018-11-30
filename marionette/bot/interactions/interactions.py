from typing import List
from ..nodes import User, Media, Hashtag, Geotag, Usertag
from ..extent import Extent


from .like import like
# from .send import send
# from .comment import comment
# from .report import report
# from .follow import follow
# from .block import block
# from .export_user import export_user
# from .export_media import export_media


class Interactions(Extent):

    input_nodes = {
              'follow': User,
              'block': User,
              'send': User,
              'export_user': User,

              'like': Media,
              'comment': Media,
              'report': Media,
              'download': Media,
              'export_media': Media,
              }

    def like(self, args):
        like(self)

    # def comment(self, args):
    #     comment(self, comments=args['comments'])
    #
    # def report(self, args):
    #     report(self)
    #
    # def follow(self, args):
    #     follow(self)
    #
    # def block(self, args):
    #     block(self)
    #
    # def send(self, args):
    #     send(self, messages=args['messages'])
    #
    # def export(self, args):
    #     if isinstance(self._acc[-1], Media):
    #         export_media(self._acc[-1], args)
    #     elif isinstance(self._acc, User):
    #         export_user(self._acc[-1], args)
