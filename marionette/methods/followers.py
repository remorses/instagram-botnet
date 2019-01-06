from typing import List
from funcy import rcompose, ignore
import time
from ..bot import Bot
from ..nodes import User, Media
from .common import accepts, cycled_api_call


@accepts(User)
def followers(bot: Bot, nodes,  args) -> List[User]:

    pack_user = lambda item: User(id=item['pk'], username=item['username'], data=item)

    process = ignore(StopIteration)(
        rcompose(
            lambda nodes: nodes.next(),
            lambda user: user.id if user.id else user.get_id(bot),
            lambda id: get_followers(bot, id),
            lambda generator: generator.next(),
            pack_user
        )
    )

    result = process(nodes)

    return result, bot.last





def get_followers( bot ,id) -> List[User]:
    return cycled_api_call(bot, bot.api.get_user_followers, id, 'users')
