from funcy import rcompose
from itertools import islice
from ..nodes import User, Media
from .common import accepts


@accepts(Media)
def authors(bot, nodes, amount, args):


    result = (media.get_author(bot) for media in nodes if bot.suitable(media))
    result = islice(result, amount)

    return result, bot.last
