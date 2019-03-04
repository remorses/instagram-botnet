from .common import decorate
from ..nodes import User

from .common import tap
from ..bot import Bot
from funcy import raiser, rcompose



@decorate(accepts=User, returns=User)
def unfollow(bot: Bot, nodes,  args):

    max = float(args['max']) if 'max' in args else float('inf')
    count = 0

    def increment():
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

    return unfollowed, {}



def unfollow_user(user, bot):
    bot.api.friendships_destroy(user.pk)
    bot.total['unfollows'] += 1
    bot.logger.info('unfollowed %s' % user)
    bot.sleep('unfollow')
