from typing import List
from .common import accepts, today
from ..nodes import Node, User, Media

@accepts(Media)
def like(bot, nodes, amount, args):

    nodes = bot.filter(nodes)

    for media in nodes:
        bot.api.like(media.id)
        if bot.last['status'] != 'ok':
            bot.logger.warn('request didn\'t return "ok" liking {}'.format(media.url))
        else:
            bot.cache['liked'].insert(dict(identifier=media.id, url=media.url, time=today()))




    return [], bot.last
