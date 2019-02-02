from .common import accepts
from ..nodes import Node, User, Media

from .common import today, tap
from ..bot import Bot
from funcy import rcompose, raiser, tap as _tap
import time



@accepts(User)
def unfollow(bot: Bot, nodes,  args):

    max = float(args['max']) if 'max' in args else 1
    count = 0

    def increment():
        bot.total['unfollows'] += 1
        nonlocal count
        count += 1

    stop = raiser(StopIteration)

    process = rcompose(
        # lambda x: tap(x, lambda: bot.logger.warn('{}._data: \n{}'.format(x, unmask(x._data)))),
        lambda x: stop() if x and count >= max else x,
        # lambda node: node \
        #     if bot.suitable(node) \
        #     else tap(None,lambda: bot.logger.warn('{} not suitable'.format(node))),
        lambda node: unfollow_user(node, bot=bot) \
            if node else None,
        lambda x: tap(x, increment) if x else None,
    )


    unfollowed = map(process, nodes)
    unfollowed = filter(lambda x: x, unfollowed)

    return unfollowed, bot.last



def unfollow_user(user, bot):
    bot.api.unfollow(user.id)
    if bot.last['status'] != 'ok':
        bot.logger.warn('request didn\'t return "ok" following {}'.format(user.username))
        bot.sleep('error')
        return None
    else:
        with bot.cache as cache:
            cache['unfollowed'].insert(dict(
                identifier=user.id,
                time=today(),
                type='user',
            ))

        bot.logger.info('unfollowed %s' % user)
        bot.sleep('unfollow')
        return user
