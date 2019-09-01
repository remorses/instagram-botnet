from ..nodes import Geotag, Media
from .common import decorate


@decorate(accepts=Media, returns=Geotag)
def geotag(bot, nodes,  args) -> Geotag:
    process = lambda media: media.location and Geotag(**media.location)
    result = map(process, nodes)
    result = filter(bool, result)
    return result, {}
