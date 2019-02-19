from funcy import rcompose
from ..nodes import Geotag, Media
from .common import accepts


@decorate(accepts=Media, returns=Geotag)
def geotag(bot, nodes,  args) -> Geotag:

    process = lambda media: media.get_geotag(bot)
    result = map(process, nodes)

    return result, {}
