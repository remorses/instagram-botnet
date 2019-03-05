from funcy import ignore, raiser, rcompose
from random import choice
from ..bot import Bot
from .common import decorate, extract_urls, substitute_vars, tap
from ..nodes import User, Node




@decorate(accepts=User, returns=Node)
def message(bot, nodes,  args):


    try:
        max = float(args['max']) if 'max' in args else float('inf')
        messages = args['messages']
    except:
        bot.logger.error('please add all necessary args, {} isn\'t enought'.format(args))
        return [], {}

    count = 0

    def increment():
        bot.total['texts'] += 1
        nonlocal count
        count += 1
        return True

    stop = raiser(StopIteration)

    send_msg_from_groups = lambda node: map(
            lambda msgs: send_message(bot, choice(msgs), node),
            messages
        ) if node else []

    process = rcompose(
        lambda x: stop() if x and count >= max else x,
        send_msg_from_groups,
        lambda arr: list(arr)[0] if list(arr) else None,
        lambda x: x and increment and x,
    )

    result = map(process, nodes)
    result = filter(lambda x: x, result)

    return result, {}




def send_message(bot: Bot, text, node, thread_id=None):

    evaluated_text = substitute_vars(text,
        receiver=node,
    )
    
    urls = extract_urls(text)
    item_type = 'link' if urls else 'text'

    res = bot.api.send_direct_item(
        item_type,
        users=[node.pk],
        text=evaluated_text,
        thread=thread_id,
        urls=urls
    )
    
    print(json.dumps(res, indent=4))
    
    bot.logger.info('texted %s' % node)
    bot.sleep('text')
    return node


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
