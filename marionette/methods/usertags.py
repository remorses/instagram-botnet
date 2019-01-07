from funcy import rcompose, take
from itertools import islice
from ..nodes import User, Media
from .common import accepts


@accepts(Media)
def usertags(bot, nodes,  args) -> User:

    process = lambda media: media.get_usertags(bot)
    result = map(process, nodes)

    return result, bot.last
