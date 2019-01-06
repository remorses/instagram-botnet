from typing import List
from funcy import rcompose
from itertools import islice
from random import uniform
import time
from ..bot import Bot
from ..nodes import User, Media
from .common import accepts, cycled_api_call


@accepts(User)
def followers(bot, nodes,  args) -> List[User]:

    pack_user = lambda item: User(id=item['pk'], username=item['username'], data=item)

    _followers = rcompose(
        lambda user: user.id if user.id else user.get_id(bot),
        lambda id: get_followers(bot, id),
    )

    result = (pack_user(item) for node in nodes for item in _followers(node) )
    # result = (user for user in result if bot.suitable(user))
    result = (user for user in result if user)


    return result, bot.last





def get_followers( bot ,id) -> List[User]:
    return cycled_api_call(bot, bot.api.get_user_followers, id, 'users')
