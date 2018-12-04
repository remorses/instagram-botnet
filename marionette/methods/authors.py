from typing import List
from ..nodes import User, Media
from .common import accepts


@accepts(Media)
def authors(bot, nodes, amount, args):

    nodes = bot.filter(nodes)

    _authors = [_author(bot, node) for node in nodes]

    return _authors, bot.last


def _author(bot, media):
    bot.api.media_info(media.id)
    data = bot.last["items"][0]["user"]
    id = data["pk"]
    return User(id=id, data=data)
