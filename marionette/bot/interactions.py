from .nodes import User, Media, Hashtag, Geotag, Usertag
from typing import List


class Interactions:

    def __init__(self, bot):
        self._accumulate = bot.accumulate
        self._bot = bot
        self._api = bot.api

    def __getitem__(self, method):
        func = getattr(self, method, False)
        if not func:
            print('not found {}'.format(method))
        return func

    def like(self, args):

        print('medias: ', self._bot._acc)

        for media in self._bot._acc:
            if isinstance(media, Media):
                id = media.id
            else:
                url = media
                id = Media.get_media_id_from_link(url)
                print('id: {}'.format(id))

            if self._api.like(id):
                print('liked media %d.' % id)
            else:
                print('can\'t like')

        self._accumulate([])

    # def media_author(self, medias: List[Media]) -> List[User]:
    #     result = []
    #     for media in medias:
    #         if self.api.media_info(media.id):
    #             author_id = str(self.api.last_json["items"][0]["user"]["pk"])
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

    def send(self, medias: List[User]):
        pass


# methods = {
#     'like': like,
#     'comment': comment,
#     'report': report,
#
#     'follow': follow,
#     'send': send,
#     'block': block
# }
