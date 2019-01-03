from funcy import rcompose, take
from itertools import islice
from ..nodes import User, Media
from .common import accepts


@accepts(Media)
def usertags(bot, nodes, amount, args) -> User:

    _usertags = rcompose(
        lambda node: node.id,
        lambda id: get_items(bot, id),
    )

    pack_user = rcompose(
        lambda data: data['user'],
        lambda data: User(username=data['username'], id=data['pk'], is_private=data['is_private'])
    )

    result = (pack_user(item) for media in nodes for item in _usertags(media))
    result = (user for user in result if bot.suitable(user))
    result = take(amount, result)

    return result, bot.last

def get_items(bot, id):
    bot.api.media_info(id)
    try:
        items = bot.last["items"][0]["usertags"]["in"]
        yield from items
    except TypeError:
        yield from []
