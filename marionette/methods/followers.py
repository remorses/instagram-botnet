from typing import List
from funcy import rcompose, ignore, tap as _tap, partial, flatten
import time
from ..bot import Bot
from ..nodes import User, Media
from .common import accepts, cycled_api_call


@accepts(User)
def followers(bot: Bot, nodes,  args) -> List[User]:

    bot.logger.debug('nodes at followers %s' % list(nodes))

    nodes = iter(list(nodes))

    pack_user = lambda item: User(id=item['pk'], username=item['username'], data=item)

    process = ignore(StopIteration, 'end')(
        rcompose(
            lambda: next(nodes),
            lambda user: user.id if user.id else user.get_id(bot),
            lambda id: cycled_api_call(bot, bot.api.get_user_followers, id, 'users'),
            lambda gen: map(pack_user, gen)

        )
    )




    result = flatten(iter(process, 'end'))




    return result, bot.last
