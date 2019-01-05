from funcy import rcompose, take
from itertools import islice
from ..nodes import Hashtag, Media
from .common import accepts


@accepts(Media)
def hashtags(bot, nodes, amount, args):

    result = (tag for media in nodes for tag in media.get_hashtags(bot))
    # result = (tag for tag in result if bot.suitable(tag))
    result = (tag for tag in result if tag)
    result = take(amount, result)

    return result, bot.last
