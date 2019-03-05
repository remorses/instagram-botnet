from funcy import ignore, raiser, rcompose
from random import choice
from ..bot import Bot
from .common import decorate, extract_urls, substitute_vars, tap
from ..nodes import User, Node
import json



@decorate(accepts=User, returns=Node)
def message(bot, nodes,  args):


    try:
        max = float(args['max']) if 'max' in args else float('inf')
        messages = args['messages']
        media = args.get('media')
        profile = args.get('profile')
        hashtag = args.get('hashtag')
    except:
        bot.logger.error('please add all necessary args, {} isn\'t enought'.format(args))
        return [], {}

    count = 0

    def increment():
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
        lambda x: increment() if x is not None else None,
    )

    result = map(process, nodes)
    result = filter(lambda x: x, result)

    return result, {}




def send_message(bot: Bot, text, node, thread_id=None):

    evaluated_text = substitute_vars(text,
        receiver=node,
    )
    
    urls = extract_urls(text)
    

    res = bot.api.send_direct_item(
        users=[node.pk],
        text=evaluated_text,
        thread=thread_id,
        urls=urls
    )
    
    print(json.dumps(res, indent=4))
    
    thread_id = res.get('payload',{}).get('thread_id', '')
    
    bot.logger.info('messaged %s' % node)
    bot.total['messages'] += 1
    bot.sleep('message')
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
