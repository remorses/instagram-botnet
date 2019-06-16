from .user_feed import user_feed
from .hashtag_feed import hashtag_feed
from .geotag_feed import geotag_feed
from ..nodes import Geotag, Hashtag, Media, User
from itertools import chain
from .common import decorate


@decorate(accepts=(User, Hashtag, Geotag,), returns=Media)
def feed(bot, nodes, args):
    
    if isinstance(nodes, (list, tuple)):
        first = nodes[0]
    else:
        first = next(nodes, None)
        nodes = chain([first], nodes)

    switch = {
        isinstance(first, User): user_feed,
        isinstance(first, Hashtag): hashtag_feed,
        isinstance(first, Geotag): geotag_feed,
    }

    if True in switch:
        return switch[True](bot, nodes, args)

    else:
        return [], {}
