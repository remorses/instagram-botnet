from .common import decorate
from ..nodes import User
from datetime import datetime
from .common import tap
from ..bot import Bot
from funcy import raiser, rcompose




@decorate(accepts=User, returns=User)
def follow(bot: Bot, nodes,  args):

    max = float(args['max']) if 'max' in args else float('inf')
    count = 0
    events = []

    def increment():
        nonlocal count
        count += 1
        
    def add_event(node: User):
        events.append({
            'type': 'follow',
            'metadata': bot.metadata,
            'node': {
                'type': 'user',
                'username': node.username,
            },
            'timestamp': str(datetime.utcnow())
        })
        return node

    stop = raiser(StopIteration)

    process = rcompose(
        lambda x: stop() if x and count >= max else x,
        lambda node: follow_user(node, bot=bot) \
            if node else None,
        lambda x: tap(x, increment) if x else None,
        lambda x: add_event(x) if x else None,
    )


    followed = map(process, nodes)
    followed = filter(lambda x: x, followed)

    return followed, { 'events': events }



def follow_user(user, bot):
    bot.api.friendships_create(user.pk)
    bot.total['follows'] += 1
    bot.logger.info(f'followed {user}')
    bot.sleep('follow')
    return user
