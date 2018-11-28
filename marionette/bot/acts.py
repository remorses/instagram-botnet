from nodes import User, Media, Hashtag, Geotag, Usertag
from typings import List


class Acts():
    def __init__(self, bot):
        self.bot = bot
        self.api = bot.api

    def like(self, medias: List[Media]):
        for media in medias:
            self.bot.api.like(media)

    def media_author(self, medias: List[Media]) -> List[User]:
        result = []
        for media in medias:
            if self.api.media_info(media.id):
                author_id = str(self.api.last_json["items"][0]["user"]["pk"])
                result += [User(id=author_id)]
        self.bot.acc = []

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
