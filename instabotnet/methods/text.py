from funcy import ignore, raiser, rcompose
from random import choice
from ..bot import Bot
from .common import decorate, extract_urls, substitute_vars, tap
from ..nodes import User, Node




@decorate(accepts=User, returns=Node)
def text(bot, nodes,  args):


    try:
        max = float(args['max']) if 'max' in args else float('inf')
        messages = args['messages']
    except Exception:
        bot.logger.error('please add all necessary args, {} isn\'t enought'.format(args))
        return [], {}

    count = 0

    def increment():
        bot.total['texts'] += 1
        nonlocal count
        count += 1

    stop = raiser(StopIteration)

    return_if_suitable = lambda node: node \
        if bot.suitable(node, table='texted', specifier=str(messages)) \
        else tap(None,lambda: bot.logger.warning('{} not suitable'.format(node)))

    discard_if_reached_limit = lambda node: node \
        if not bot.reached_limit('texts') \
        else tap(None, bot.logger.error('reached texting daily limit'))

    send_msg_from_groups = lambda node: map(
            lambda msgs: send_message(bot, choice(msgs), node),
            messages) \
         if node else []



    process = rcompose(
        lambda x: stop() if x and count >= max else x,
        # return_if_suitable,
        discard_if_reached_limit,
        send_msg_from_groups,
        lambda arr: list(arr)[0] if arr else None,
        lambda x: tap(x, increment) if x else None,
    )


    result = map(process, nodes)
    result = filter(lambda x: x, result)

    return result, {}




def send_message(bot: Bot, text, node, thread_id=None):

    evaluated_text = substitute_vars(text,
        receiver=ignore(AttributeError, '')(
            lambda: node.get_username(bot).username
        )(),
        bio=node.get_bio(bot),
    )

    user_id = node.pk if node.pk else node.get_id(bot)
    urls = extract_urls(text)
    item_type = 'link' if urls else 'text'

    bot.api.send_direct_item(
        item_type,
        users=[str(user_id)],
        text=evaluated_text,
        thread=thread_id,
        urls=urls
    )
    if bot.last['status'] == 'ok':
        bot.logger.debug('texted %s' % node)
        bot.sleep('text')
        return node
    else:
        bot.logger.error("message to {} wasn't sent".format(node))
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
