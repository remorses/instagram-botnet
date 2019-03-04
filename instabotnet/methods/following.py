from typing import List
from funcy import rcompose, mapcat
from ..nodes import User
from .common import decorate, cycled_api_call


@decorate(accepts=User, returns=User)
def following(bot, nodes,  args) -> List[User]:

    amount = args.get('amount') or 1

    pack_user = lambda item: User(**item)

    process = rcompose(
        lambda user: user.pk,
        lambda id: cycled_api_call(amount, bot, bot.api.user_following, dict(user_id=id, **args.get('query', {}),), 'users'),
        lambda gen: map(pack_user, gen)
    )

    result = mapcat(process, nodes)

    return result, {}
