from .common import accepts
from ..nodes import Node, User, Media
from ..debug import unmask
from .common import today, tap
from ..bot import Bot
from funcy import rcompose, raiser, tap as _tap
import time



@accepts(User)
def follow(bot: Bot, nodes,  args):

    count = 0

    def increment():
        nonlocal count
        count += 1

    stop = raiser(StopIteration)

    process = rcompose(
        # lambda x: tap(x, lambda: bot.logger.warn('{}._data: \n{}'.format(x, unmask(x._data)))),
        lambda node: node \
            if bot.suitable(node) \
            else tap(None,lambda: bot.logger.warn('{} not suitable'.format(node))),
        lambda node: follow_user(node, bot=bot) \
            if node else None,
        lambda x: tap(x, increment) if x else None,
        lambda x: stop() if x and count >= float(args['amount']) else x,
    )


    followed = map(process, nodes)
    followed = filter(lambda x: x, followed)
    followed = list(followed)

    return followed, bot.last



def follow_user(user, bot):
    bot.api.follow(user.id)
    if bot.last['status'] != 'ok':
        bot.logger.warn('request didn\'t return "ok" following {}'.format(user.username))
        time.sleep(bot.delay['error'])
        return None
    else:
        with bot.cache as cache:
            cache['followed'].insert(dict(identifier=user.id, time=today(), type='user', interaction='follow'))

        bot.logger.info('followed %s' % user)
        time.sleep(bot.delay['follow'])
        return user
