from nodes import User, Media, Hashtag, Geotag, Usertag
from typings import List


def like(users: List[Media]):
    pass


def comment(users: List[Media]):
    pass


def report(users: List[Media]):
    pass


def follow(med: List[User]):
    pass


def block(med: List[User]):
    pass


def send(med: List[User]):
    pass


methods = {
    'like': like,
    'comment': comment,
    'report': report,

    'follow': follow,
    'send': send,
    'block': block
}
