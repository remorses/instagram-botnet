from typing import List
from funcy import rcompose
from itertools import islice
from random import uniform
import time
from ..bot import Bot
from ..nodes import User, Media
from .common import accepts


@accepts(User)
def following(bot, nodes, amount, args) -> List[User]:


    pack_user = lambda item: User(id=item['pk'], username=item['username'])

    _following = rcompose(
        lambda user: user.id if user.id else user.get_id(bot),
        lambda id: get_following(bot, id, amount),
    )

    result = (pack_user(item) for node in nodes for item in _following(node) )
    result = (user for user in result if bot.suitable(user))
    result = islice(result, amount)

    return result, bot.last



def get_following( bot ,id,  amount) -> List[User]:

    next_max_id = ''
    sleep_track = 0
    done = 0

    while True:
        try:
            bot.api.get_user_followings(id, next_max_id)
            items = bot.last["users"] if 'users' in bot.last else []

            if len(items) <= amount:
                yield from items
                done += len(items)
                return

            elif (done + len(items)) >= amount:
                yield from items[:amount - done]
                done += len(items)
                return

            else:
                yield from items
                done += len(items)

        except Exception:
            return

        if sleep_track > 10:
            bot.logger.debug('sleeping some time while getting following')
            time.sleep(bot.delay['getter'])
            sleep_track = 0

        next_max_id = bot.last.get("next_max_id", "")
        sleep_track += 1
