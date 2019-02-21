from funcy import mapcat
from itertools import islice
from ..nodes import Hashtag, Media
from .common import decorate


@decorate(accepts=Media, returns=Hashtag)
def hashtags(bot, nodes,  args):

    amount = args.get('amount')
    process = lambda media: media.get_hashtags(bot)
    result = mapcat(process, nodes)
    result = islice(result, amount)

    return result, {}
