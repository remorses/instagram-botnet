from funcy import rcompose
from itertools import islice
from ..nodes import User, Media
from .common import accepts


@accepts(Media)
def authors(bot, nodes,  args):


    process = lambda media: media.get_author(bot)
    result = map(process, nodes)

    return result, bot.last
