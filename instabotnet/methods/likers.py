
from typing import List
from funcy import  rcompose, mapcat
from ..bot import Bot
from ..nodes import  Media, User
from .common import decorate




@decorate(accepts=Media, returns=User)
def likers(bot, nodes,  args) -> List[Media]:

    pack_user = lambda item: User(**item)
    amount = args.get('amount')

    process = rcompose(
            lambda media: media.pk,
            lambda id: get_likers(id, bot, amount),
            lambda gen: map(pack_user, gen)
        )

    result = mapcat(process, nodes)


    return result, {}





def get_likers(id, bot: Bot, amount):
    data = bot.api.media_likers(id)
    if 'users' in data:
        yield from data['users'][:amount]
    else:
        yield from []
