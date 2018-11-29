from typing import List
from ..extent import Extent
from ..nodes import User, Media, Comment, Hashtag, Usertag, Geotag


from .user_feed import user_feed
from .geotag_feed import geotag_feed
from .hashtag_feed import hashtag_feed


class EdgeException(Exception):
    pass


class Edges(Extent):

    def author(self, args):
        result = []
        for media in self._acc:
            if self._api.media_info(media.id):
                author_id = str(self._api.last_json["items"][0]["user"]["pk"])
                result += [User(id=author_id)]
        self._accumulate(result)

    def user_following(self, args):
        pass

    def feed(self, args):
        if isinstance(self._acc, User) or 'id' in self._acc:
            user_feed(self)

        if isinstance(self._acc, Geotag) or 'id' in self._acc:
            user_feed(self)

        if isinstance(self._acc, Hashtag) or 'id' in self._acc:
            user_feed(self)

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
