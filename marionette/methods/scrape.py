from .common import accepts
from ..nodes import Node, User, Media
from ..debug import unmask
from .common import today, tap
from ..bot import Bot
from funcy import rcompose, raiser, tap as _tap
import time



@accepts(Node)
def scrape(bot: Bot, nodes,  args):

    count = 0

    def increment():
        global count
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
        lambda x: stop() if x and count >= args['amount'] else None,
    )


    list(map(process, nodes))

    return [], bot.last
