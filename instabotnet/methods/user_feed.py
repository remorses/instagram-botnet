
from typing import List
from funcy import  rcompose, mapcat
from ..nodes import User, Media
from .common import accepts, cycled_api_call, tap

@accepts(User)
def user_feed(bot, nodes,  args) -> List[Media]:
    amount = args.get('amount')

    pack_media = lambda data: Media(id=data['pk'], data=data)

    process = rcompose(
        lambda user: user.id if user.id else user.get_id(bot),
        lambda id: cycled_api_call(amount, bot, bot.api.get_user_feed, id, 'items'),
        lambda items: map(pack_media, items),
        # lambda x: tap(x, lambda: print(x)),

    )

    result = mapcat(process, nodes)

    return result, bot.last
