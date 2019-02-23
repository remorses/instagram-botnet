from .common import decorate
from ..nodes import User

from .common import tap
from ..bot import Bot
from funcy import raiser, rcompose



@decorate(accepts=User, returns=User)
def follow(bot: Bot, nodes,  args):

    max = float(args['max']) if 'max' in args else float('inf')
    count = 0

    def increment():
        bot.total['follows'] += 1
        nonlocal count
        count += 1

    stop = raiser(StopIteration)

    process = rcompose(
        # lambda x: tap(x, lambda: bot.logger.warn('{}._data: \n{}'.format(x, unmask(x._data)))),
        lambda x: stop() if x and count >= max else x,
        # lambda node: node \
        #     if bot.suitable(node) \
        #     else tap(None,lambda: bot.logger.warn('{} not suitable'.format(node))),
        lambda node: follow_user(node, bot=bot) \
            if node else None,
        lambda x: tap(x, increment) if x else None,
    )


    followed = map(process, nodes)
    followed = filter(lambda x: x, followed)

    return followed, {}



def follow_user(user, bot):
    data = bot.api.friendship_create(user.id)
    bot.total['follows'] += 1
    bot.logger.info(f'followed {user}')
    return user
