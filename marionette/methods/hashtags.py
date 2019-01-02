from funcy import rcompose, take
from itertools import islice
from ..nodes import Hashtag, Media
from .common import accepts


@accepts(Media)
def hashtags(bot, nodes, amount, args):

    _hashtags = rcompose(
        lambda node: node.id,
        lambda id: get_caption(bot, id),
        lambda text: get_tags(text,)
    )

    pack_hashtag = lambda tag: Hashtag(name=tag)

    result = (pack_hashtag(tag) for media in nodes for tag in _hashtags(media))
    result = (tag for tag in result if bot.suitable(tag))
    result = take(amount, result)

    return result, bot.last

def get_tags(text):
    yield from set(part[1:] for part in text.split() if part.startswith('#'))

def get_caption(bot, id):
    bot.api.media_info(id)
    data = bot.last["items"][0]["caption"]['text']
    return data
