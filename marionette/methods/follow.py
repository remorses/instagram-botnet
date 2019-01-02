from .common import accepts
from ..nodes import Node, User, Media
from .common import today
from ..bot import Bot

@accepts(User)
def follow(bot: Bot, nodes, amount, args):

    nodes = bot.filter(nodes)

    for user in nodes:
        bot.api.follow(user.id)
        if bot.last['status'] != 'ok':
            bot.logger.warn('request didn\'t return "ok" following {}'.format(user.username))
        else:
            bot.cache['followed'].insert(dict(identifier=user.id, time=today()))

    data = bot.last

    return [], data
