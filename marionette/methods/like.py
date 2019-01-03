from typing import List
from .common import accepts, today
from ..nodes import Node, User, Media
from time import time
@accepts(Media)
def like(bot, nodes, amount, args):

    for media in nodes[:amount]:
        bot.api.like(media.id)
        if bot.last['status'] != 'ok':
            bot.logger.warn('request didn\'t return "ok" liking {}'.format(media.url))
            time.sleep(bot.delay['error'])
        else:
            with bot.cache as cache:
                cache['liked'].insert(dict(identifier=media.id, url=media.url, time=today(), type='media'))

            bot.logger.debug('sleeping some time')
            time.sleep(bot.delay['like'])




    return [], bot.last
