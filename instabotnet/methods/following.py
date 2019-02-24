from typing import List
from funcy import rcompose, mapcat
from ..nodes import User
from .common import decorate, cycled_api_call


@decorate(accepts=User, returns=User)
def following(bot, nodes,  args) -> List[User]:

    pack_user = lambda item: User(id=item['pk'], username=item['username'], data=item)
    amount = args.get('amount')

    process = rcompose(
        lambda user: user.id if user.id else user.get_id(bot),
        lambda id: cycled_api_call(amount, bot, bot.api.user_following, id, 'users'),
        lambda gen: map(pack_user, gen)
    )

    result = mapcat(process, nodes)

    return result, {}
