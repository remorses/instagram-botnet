from typing import List
from funcy import  rcompose, raiser, ignore, mapcat, partial, tap as _tap
import time
from random import choice
from ..bot import Bot
from .common import accepts, today, tap, extract_urls, substitute_vars
from ..nodes import Node, User, Media




@accepts(Media)
def comment(bot, nodes,  args):

    try:
        max = float(args['max']) if 'max' in args else float('inf')
        comments = args['comments']
    except:
        bot.logger.error('please add all necessary args, {} isn\'t enought'.format(args))
        return [], {}

    count = 0



    def increment():
        bot.total['comments'] += 1
        nonlocal count
        count += 1

    stop = raiser(StopIteration)

    def store_in_cache(node):
        with bot.cache as cache:
            cache['commented'].insert(
                dict(identifier=node.id,
                    specifier=str(comments),
                    time=today(),
                    type='media')
            )
        return node

    return_if_suitable = lambda node: node \
        if bot.suitable(node, table='commented', specifier=str(comments)) \
        else tap(None,lambda: bot.logger.warn('{} not suitable'.format(node)))

    discard_if_reached_limit = lambda node: node \
        if not bot.reached_limit('comments') \
        else tap(None, bot.logger.error('reached commenting daily limit'))

    do_comment_from_groups = lambda node: map(
            lambda cmnts: do_comment(bot, choice(cmnts), node),
            comments) \
         if node else []



    process = rcompose(
        lambda x: stop() if x and count >= max else x,
        return_if_suitable,
        discard_if_reached_limit,
        do_comment_from_groups,
        lambda arr: list(arr)[0] if arr else None,
        lambda node: store_in_cache(node) if node else None,
        lambda x: tap(x, increment) if x else None,
    )


    result = map(process, nodes)
    result = filter(lambda x: x, result)

    return result, bot.last




def do_comment(bot: Bot, text, node, thread_id=None):

    media_id = node.id
    evaluated_text = substitute_vars(text,
        author=ignore(AttributeError, '')(
            lambda: node.get_author(bot).username
        )(),
        caption=node.get_caption(bot),
        geotag=ignore(AttributeError, '')(
            lambda: node.get_geotag(bot).name or ''
        )(),
        usertags=ignore(AttributeError, '')(
            lambda: list(map(lambda x: x.get_username(bot), node.get_usertags(bot))) or []
        )()
    )

    bot.api.comment(
        media_id=media_id,
        comment_text=evaluated_text,
    )
    if bot.last['status'] == 'ok':
        bot.logger.debug('commented %s' % node)
        bot.sleep('comment')
        return node
    else:
        bot.logger.error("comment to {} wasn't posted".format(node))
        bot.sleep('error')
        return None
