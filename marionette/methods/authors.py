from funcy import rcompose
from itertools import islice
from ..nodes import User, Media
from .common import accepts


@accepts(Media)
def authors(bot, nodes, amount, args):

    process = rcompose(
        lambda node: node.id,
        lambda id: get_author(bot, id),
    )

    result = (process(media) for media in nodes if bot.suitable(media))
    
    result = islice(result, amount)


    return result, bot.last


def get_author(bot, id):
    bot.api.media_info(id)
    data = bot.last["items"][0]["user"]
    id = data["pk"]
    username = data["username"]
    return User(id=id, username=username, data=data)
