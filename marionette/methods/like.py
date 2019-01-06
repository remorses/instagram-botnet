from typing import List
from funcy import take, rcompose
import time
from .common import accepts, today, tap
from ..nodes import Node, User, Media




@accepts(Media)
def like(bot, nodes,  args):


    count = 0

    def increment():
        global count
        count += 1

    process = rcompose(
        lambda node: node if bot.suitable(node) else tap(None,
            lambda: bot.logger.warn('{} not suitable'.format(node))),
        lambda x: tap(x, increment) if x else None,
        lambda node: _like(node, bot=bot) \
            if count <= args['amount'] and node else None,
    )

    [process(node) for node in nodes if node]

    data = bot.last
    return [], data


def _like(media, bot):
        bot.api.like(media.id)
        if bot.last['status'] != 'ok':
            bot.logger.warn('request didn\'t return "ok" liking {}'.format(media.url))
            time.sleep(bot.delay['error'])
        else:
            with bot.cache as cache:
                cache['liked'].insert(dict(identifier=media.id, url=media.url, time=today(), type='media', interaction='like'))

            bot.logger.debug('liked %s' % media.url)
            time.sleep(bot.delay['like'])
