from typing import List
from funcy import rcompose
from itertools import islice
from random import uniform
import time
from ..bot import Bot
from ..nodes import User, Media
from .common import accepts, get_cycled_api


@accepts(User)
def followers(bot, nodes, amount, args) -> List[User]:

    pack_user = lambda item: User(id=item['pk'], username=item['username'], data=item)

    _followers = rcompose(
        lambda user: user.id if user.id else user.get_id(bot),
        lambda id: get_followers(bot, id, amount),
    )

    result = (pack_user(item) for node in nodes for item in _followers(node) )
    # result = (user for user in result if bot.suitable(user))
    result = (user for user in result if user)
    result = islice(result, amount)

    return result, bot.last





def get_followers( bot ,id,  amount) -> List[User]:
    return get_cycled_api(bot, bot.api.get_user_followers, id, 'users', amount)
