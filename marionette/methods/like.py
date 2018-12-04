from typing import List
from .common import accepts
from ..nodes import Node, User, Media


@accepts(Media)
def like(bot, nodes, amount, args):

    nodes = bot.filter(nodes)

    for node in nodes:
        bot.api.like(node.id)
        if bot.last['status'] == 'ok':
            bot.logger.info('liked success')

    data = bot.last

    return [], data
