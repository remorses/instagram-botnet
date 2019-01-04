from .common import accepts
from ..nodes import Node, User, Media
from .common import today
from ..bot import Bot
import time

@accepts(User)
def follow(bot: Bot, nodes, amount, args):

    for user in nodes:
        bot.api.follow(user.id)
        if bot.last['status'] != 'ok':
            bot.logger.warn('request didn\'t return "ok" following {}'.format(user.username))
            time.sleep(bot.delay['error'])
        else:
            with bot.cache as cache:
                cache['followed'].insert(dict(identifier=user.id, time=today(), type='user', interaction='follow'))

            bot.logger.debug('followed %s' % user.id)
            time.sleep(bot.delay['follow'])


    data = bot.last

    return [], data
