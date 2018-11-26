# Edges
from typings import TypeVar, List, Union

from nodes import User, Media, Comment, Hashtag, Usertag, Geotag


T = TypeVar('T')
Input = Union[T, List[T]]


def is_right_input(input, type):
    if isinstance(input, type):
        return True
    else:
        return False


def assert_input_type(fun):
    def wrapper(*args, **nargs):
        input_type = fun.__annotations__.input
        if(not is_right_input(input, input_type)):
            error = "wrong edge, " + fun.__name__ + \
                "accepts only " + input_type
            raise Exception(error)
        return fun(*args, **nargs)


class Edges:

    def __init__(self):
        pass

    def user_followers(self, input: Input[User]) -> List[User]:
        pass

    def user_following(self, user: Input[User]) -> List[User]:
        pass

    def user_feed(self, user: Input[User]) -> List[Media]:
        pass

    def media_author(self, media: Input[Media]) -> List[User]:
        pass

    def media_likers(self, media: Input[Media]) -> List[User]:
        pass

    def media_commenters(self, media: Input[Media]) -> List[User]:
        pass

    def media_comments(self, media: Input[User]) -> List[Comment]:
        pass

    def media_hashtags(self, media: Input[User]) -> List[Hashtag]:
        pass

    def media_usertags(self, media: Input[Media]) -> List[Usertag]:
        pass

    def hashtag_feed(self, hashtag: Input[Hashtag]) -> List[Media]:
        pass

    def geotag_feed(self, geotag: Input[Geotag]) -> List[Media]:
        pass
