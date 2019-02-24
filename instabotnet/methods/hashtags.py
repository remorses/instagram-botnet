from funcy import mapcat
from itertools import islice
from ..nodes import Hashtag, Media
from .common import decorate


@decorate(accepts=Media, returns=Hashtag)
def hashtags(bot, nodes,  args):

    amount = args.get('amount')

    def process(node):
        text = node._data['caption']['text']
        raw_tags = set(part[1:] for part in text.split() if part.startswith('#'))
        tags = (Hashtag(name=tag) for tag in raw_tags)
        yield from tags


    result = mapcat(process, nodes)
    result = islice(result, amount)

    return result, {}
