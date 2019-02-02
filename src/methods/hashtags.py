from funcy import rcompose, mapcat
from itertools import islice
from ..nodes import Hashtag, Media
from .common import accepts


@accepts(Media)
def hashtags(bot, nodes,  args):

    amount = args.get('amount')
    process = lambda media: media.get_hashtags(bot)
    result = mapcat(process, nodes)
    result = islice(result, amount)

    return result, bot.last
