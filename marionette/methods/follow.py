from .common import accepts
from ..nodes import Node, User, Media
from ..bot import Bot

@accepts(User)
def follow(bot: Bot, nodes, amount, args):

    nodes = bot.filter(nodes)

    for user in nodes:
        bot.api.follow(user.id)
        if bot.last['status'] == 'ok':
            bot.logger.info('followed user {}'.format(user.username))

    data = bot.last

    return [], data
