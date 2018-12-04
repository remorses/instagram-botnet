from .common import accepts
from ..nodes import Node, User, Media
from ..bot import Bot

@accepts(User)
def follow(bot: Bot, nodes, amount, args):

    nodes = bot.filter(nodes)

    for node in nodes:
        bot.api.follow(node.id)
        if bot.last['status'] == 'ok':
            bot.logger.info('follow success')

    data = bot.last

    return [], data
