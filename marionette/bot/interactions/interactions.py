from typing import List
from ..nodes import User, Media, Hashtag, Geotag, Usertag
from ..extent import Extent


from .like import like
from .send import send


class Interactions(Extent):

    input_types = {
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

    # def media_author(self, medias: List[Media]) -> List[User]:
    #     result = []
    #     for media in medias:
    #         if self._api.media_info(media.id):
    #             author_id = str(self._api.last_json["items"][0]["user"]["pk"])
    #             result += [User(id=author_id)]
    #     self._accumulate([])

    def comment(self, users: List[Media]):
        pass

    def report(self, users: List[Media]):
        pass

    def follow(self, medias: List[User]):
        pass

    def block(self, medias: List[User]):
        pass

    def send(self, args):
        send(self, args)


# methods = {
#     'like': like,
#     'comment': comment,
#     'report': report,
#
#     'follow': follow,
#     'send': send,
#     'block': block
# }
