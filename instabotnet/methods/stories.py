from .geotag_stories import geotag_stories
from .user_stories import user_stories
from .hashtag_stories import hashtag_stories
from ..nodes import Geotag, Hashtag, Media, User
from itertools import chain
from .common import decorate


@decorate(accepts=(User, Hashtag, Geotag,), returns=Media)
def stories(bot, nodes, args):
    
    if isinstance(nodes, (tuple, list)):
        first = nodes[0]
    else:
        first = next(nodes, None)
        nodes = chain([first], nodes)

    switch = {
        isinstance(first, User): user_stories,
        isinstance(first, Hashtag): hashtag_stories,
        isinstance(first, Geotag): geotag_stories,
    }

    if True in switch:
        return switch[True](bot, nodes, args)

    else:
        return [], {}
