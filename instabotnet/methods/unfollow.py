from .common import decorate
from ..nodes import User
from datetime import datetime
from .common import tap
from ..bot import Bot
from funcy import raiser, rcompose



@decorate(accepts=User, returns=User)
def unfollow(bot: Bot, nodes,  args):

    max = float(args['max']) if 'max' in args else float('inf')
    count = 0
    events = []

    def add_event(node: User):
        events.append({
            'type': 'unfollow',
            'metadata': bot.metadata,
            'args': {},
            'node': {
                'type': 'user',
                'username': node.username,
            },
            'timestamp': str(datetime.utcnow())
        })
        return node
    

    def increment():
        nonlocal count
        count += 1
        return True

    stop = raiser(StopIteration)

    process = rcompose(
        lambda x: stop() if x and count >= max else x,
        lambda node: unfollow_user(node, bot=bot) \
            if node else None,
        lambda x: x and increment() and x,
        lambda x: x and add_event(x) and x
    )


    unfollowed = map(process, nodes)
    unfollowed = filter(lambda x: x, unfollowed)

    return unfollowed, { 'events': events }



def unfollow_user(user, bot):
    bot.api.friendships_destroy(user.pk)
    bot.total['unfollows'] += 1
    bot.logger.info('unfollowed %s' % user)
    bot.sleep('unfollow')
    return user
