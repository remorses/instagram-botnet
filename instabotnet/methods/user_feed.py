
from typing import List
from funcy import  rcompose, mapcat
from ..nodes import User, Media
from ..bot import Bot
from .common import cycled_api_call, decorate, tap




@decorate(accepts=User, returns=Media)
def user_feed(bot: Bot, nodes,  args) -> List[Media]:

    amount = args.get('amount')

    pack_media = lambda data: Media(**data)

    process = rcompose(
        lambda user: user.username,
        # lambda x: tap(x, lambda: print(x)),
        lambda name: cycled_api_call(amount, bot, bot.api.username_feed, name, 'items'),
        lambda items: map(pack_media, items),
        # lambda x: tap(x, lambda: print(x)),

    )

    result = mapcat(process, nodes)

    return result, {}
