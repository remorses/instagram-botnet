from typing import List
from ..extent import Extent
from ..nodes import User, Media, Comment, Hashtag, Usertag, Geotag


from .user_feed import user_feed
from .geotag_feed import geotag_feed
from .hashtag_feed import hashtag_feed


class EdgeException(Exception):
    pass


class Edges(Extent):

    input_types = {
              'following': User,
              'followers': User,
              'user_feed': User,

              'author': Media,
              'comments': Media,
              'commenters': Media,
              'hashtags': Media,
              'geotag': Media,
              'usertags': Media,

              'geotag_feed': Geotag,
              'hashtag_feed': Hashtag
              }

    def author(self, args):
        result = []
        for media in self._acc:
            if self._api.media_info(media.id):
                author_id = str(self._api.last_json["items"][0]["user"]["pk"])
                result += [User(id=author_id)]
        self._accumulate(result)

    def following(self, args):
        pass

    def followers(self, args):
        pass

    def feed(self, args):
        if isinstance(self._acc, User) or 'id' in self._acc:
            user_feed(self)

        if isinstance(self._acc, Geotag) or 'id' in self._acc:
            user_feed(self)

        if isinstance(self._acc, Hashtag) or 'id' in self._acc:
            user_feed(self)

    def user_feed(self, args):
        user_feed(self)

    def geotag_feed(self, args):
        geotag_feed(self)

    def hashtag_feed(self, args):
        hashtag_feed(self)

    def likers(self, args):
        pass

    def commenters(self, args):
        pass

    def comments(self, args):
        pass

    def hashtags(self, args):
        pass

    def usertags(self):
        pass
