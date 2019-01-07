from funcy import rcompose, take
from itertools import islice
from ..nodes import Hashtag, Media
from .common import accepts


@accepts(Media)
def hashtags(bot, nodes,  args):

    process = lambda media: media.get_hashtags(bot)
    result = map(process, nodes)

    return result, bot.last
