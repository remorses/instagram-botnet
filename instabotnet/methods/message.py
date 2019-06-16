from funcy import ignore, raiser, rcompose
from random import choice
from ..bot import Bot
from .common import decorate, extract_urls, substitute_vars, tap
from ..nodes import User, Node
import json
from datetime import datetime


@decorate(accepts=User, returns=Node)
def message(bot, nodes,  args):

    try:
        max = float(args['max']) if 'max' in args else float('inf')
        messages = args['messages']
        media = args.get('media_share')
        profile = args.get('profile')
        hashtag = args.get('hashtag')
    except Exception:
        bot.logger.error('please add all necessary args, {} isn\'t enought'.format(args))
        return [], {}

    count = 0
    events = []

    def increment():
        nonlocal count
        count += 1
        return True

    def add_event(pair):
        node, text = pair
        events.append({
            'type': 'message',
            'metadata': bot.metadata,
            'args': {
                'message': text,
            },
            'node': {
                'type': 'user',
                'username': node.username,
            },
            'timestamp': str(datetime.utcnow())
        })
        return node

    stop = raiser(StopIteration)

    listmap = rcompose(map, list)

    process = rcompose(
        lambda x: stop() if x and count >= max else x,
        lambda x: (x, listmap(choice, messages)),
        lambda pair: listmap(lambda m: send_message(bot, m, pair[0]), pair[1]),
        # lambda x: print(x) or x,
        lambda x: listmap(add_event, x),
        lambda x: x and x[0],
        lambda x: x and increment() and x,
        
    )

    result = map(process, nodes)
    result = filter(lambda x: x, result)

    return result, { 'events': events }




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
    
    # print(json.dumps(res, indent=4))
    
    thread_id = res.get('payload',{}).get('thread_id', '')
    
    bot.logger.info('messaged %s' % node)
    bot.total['messages'] += 1
    bot.sleep('message')
    return (node, text)


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
