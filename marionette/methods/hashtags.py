from funcy import rcompose, mapcat
from ..nodes import Hashtag, Media
from .common import accepts


@accepts(Media)
def hashtags(bot, nodes,  args):

    process = lambda media: media.get_hashtags(bot)
    result = mapcat(process, nodes)

    return result, bot.last
