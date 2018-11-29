from typing import List
from .nodes import User, Media, Hashtag, Geotag, Usertag
from .connection import Connection


class Interactions(Connection):

    def like(self, args):

        print('medias: ', self._acc)

        for media in self._acc:
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

        self._reset()

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
