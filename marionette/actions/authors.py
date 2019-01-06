from funcy import rcompose
from itertools import islice
from ..nodes import User, Media
from .common import accepts


@accepts(Media)
def authors(bot, nodes,  args):


    result = (media.get_author(bot) for media in nodes if media)


    return result, bot.last
