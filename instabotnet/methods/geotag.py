from ..nodes import Geotag, Media
from .common import decorate


@decorate(accepts=Media, returns=Geotag)
def geotag(bot, nodes,  args) -> Geotag:

    process = lambda media: Geotag(**media.location)

    result = map(process, nodes)


    return result, {}
