from typing import List
from funcy import mapcat, rcompose
from ..bot import Bot
from ..nodes import User
from .common import decorate, cycled_api_call


@decorate(accepts=User, returns=User)
def followers(bot: Bot, nodes,  args) -> List[User]:

    # bot.logger.debug('nodes at followers %s' % list(nodes)[:3])
    #
    # nodes = iter(list(nodes))
    amount = args.get('amount') or 1
    # query = args.get('query', {})

    pack_user = lambda item: User(**item)

    process = rcompose(
            lambda user: user.pk,
            lambda id: cycled_api_call(
                amount,
                bot,
                bot.api.user_followers,
                dict(user_id=id, **args.get('query', {}),) ,
                'users',
            ),
            lambda gen: map(pack_user, gen)

        )

    result = mapcat(process, nodes)

    return result, {}
