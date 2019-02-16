from funcy import rcompose, mapcat
from ..nodes import User, Media
from .common import accepts


@accepts(Media)
def authors(bot, nodes,  args):


    process = lambda media: media.get_author(bot)
    result = mapcat(process, nodes)

    return result, {}
