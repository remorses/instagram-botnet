from .user_feed import userfeed
from .hashtag_feed import hashtag_feed
from .geotag_feed import geotag feed
from ..nodes import Node, User, Hashtag, Geotag


@accepts((User, Hashtag, Geotag))
def feed(bot, nodes, args):
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
        return []