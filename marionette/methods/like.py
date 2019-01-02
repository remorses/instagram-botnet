from typing import List
from .common import accepts
from ..nodes import Node, User, Media


@accepts(Media)
def like(bot, nodes, amount, args):

    nodes = bot.filter(nodes)

    for media in nodes:
        bot.api.like(media.id)
        if bot.last['status'] != 'ok':
            bot.logger.warn('request didn\'t return "ok" following {}'.format(media.url))


    return [], bot.last
