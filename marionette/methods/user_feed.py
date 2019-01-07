
from typing import List
from funcy import  rcompose, mapcat
from ..nodes import User, Media
from .common import accepts, cycled_api_call

@accepts(User)
def user_feed(bot, nodes,  args) -> List[Media]:

    pack_media = lambda data: Media(id=data['pk'], data=data)

    process = rcompose(
        lambda user: user.id if user.id else user.get_id(bot),
        # lambda x: tap(x, lambda: print(bot.last)),
        lambda id: cycled_api_call(bot, bot.api.get_user_feed, id, 'items'),
        lambda items: map(pack_media, items),
    )

    result = mapcat(process, nodes)

    return result, bot.last
