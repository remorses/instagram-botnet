# Edges
from typing import List
from .connection import Connection
from .nodes import User, Media, Comment, Hashtag, Usertag, Geotag


# def assert_List_type(fun):
#     def wrapper(*args, **nargs):
#         List_type = fun.__annotations__.List
#         if(not is_right_List(List, List_type)):
#             error = "wrong edge, " + fun.__name__ + \
#                 "accepts only " + List_type
#             raise Exception(error)
#         return fun(*args, **nargs)


class EdgeException(Exception):
    pass


class Edges(sdfh):

    def __init__(self, bot):
        self._acc = bot.acc
        self._accumulate = bot.accumulate
        self._api = bot.api

    def __getitem__(self, method):
        return getattr(self, method)

    def media_author(self, args) -> List[User]:
        result = []
        for media in self.acc:
            if self._api.media_info(media.id):
                author_id = str(self._api.last_json["items"][0]["user"]["pk"])
                result += [User(id=author_id)]
        self._accumulate(result)

    def user_following(self, user: List[User]) -> List[User]:
        pass

    def user_feed(self, user: List[User]) -> List[Media]:
        pass

    def media_likers(self, media: List[Media]) -> List[User]:
        pass

    def media_commenters(self, media: List[Media]) -> List[User]:
        pass

    def media_comments(self, media: List[User]) -> List[Comment]:
        pass

    def media_hashtags(self, media: List[User]) -> List[Hashtag]:
        pass

    def media_usertags(self, media: List[Media]) -> List[Usertag]:
        pass

    def hashtag_feed(self, hashtag: List[Hashtag]) -> List[Media]:
        pass

    def geotag_feed(self, geotag: List[Geotag]) -> List[Media]:
        pass
