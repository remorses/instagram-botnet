from typing import List
from funcy import  rcompose, raiser, ignore, mapcat
import time
from random import choice
from ..bot import Bot
from .common import accepts, today, tap, extract_urls
from ..nodes import Node, User, Media




@accepts(Media)
def text(bot, nodes,  args):


    try:
        amount = float(args['amount']) if 'amount' in args else 1
        messages = args['messages']
    except:
        bot.logger.error('please add all necessary args, {} isn\'t enought'.format(args))
        return [], {}


    count = 0

    def increment():
        bot.total['texts'] += 1
        nonlocal count
        count += 1

    stop = raiser(StopIteration)

    send_from_groups = lambda node, messages: map(
            lambda msg: send_message(node, choice(msg), bot=bot),
            messages
        )

    def store_in_cache(node):
        with bot.cache as cache:
            cache['texted'].insert(
                dict(identifier=node.id,
                    specifier=str(messages),
                    time=today(),
                    type='user')
            )

    process = rcompose(
        lambda node: node \
            if bot.suitable(node, table='texted', specifier=str(messages)) \
            else tap(None,lambda: bot.logger.warn('{} not suitable'.format(node))),
        lambda node: node \
            if not bot.reached_limit('texts') \
            else tap(None, bot.logger.error('reached send messages daily limit')),
        lambda node: send_from_groups(node, messages) \
            if node else None,
        lambda node: store_in_cache(node)
            if node
            else None,
        lambda x: tap(x, increment) if x else None,
        lambda x: stop() if x and count >= amount + 1 else x,
    )


    result = mapcat(process, nodes)
    result = filter(lambda x: x, result)

    return result, bot.last




def send_message(bot: Bot, text, node, thread_id=None):

    user_id = node.id if node.id else node.get_id(bot)

    urls = extract_urls(text)
    item_type = 'link' if urls else 'text'

    if bot.api.send_direct_item(
        item_type,
        user_ids=[user_id],
        text=text,
        thread=thread_id,
        urls=urls
    ):
        bot.logger.debug('texted %s' % node)
        bot.sleep('text')
        return node
    else:
        bot.logger.error("message to {user_ids} wasn't sent".format(user_ids=node))
        bot.sleep('error')
        return None


# def send_messages(bot, text, user_ids):
#     broken_items = []
#     if not user_ids:
#         bot.logger.info("User must be at least one.")
#         return broken_items
#     bot.logger.info("Going to send %d messages." % (len(user_ids)))
#     for user in tqdm(user_ids):
#         if not bot.send_message(text, user):
#             bot.error_delay()
#             broken_items = user_ids[user_ids.index(user):]
#             break
#     return broken_items
