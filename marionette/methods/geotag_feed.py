
from typing import List
from funcy import  rcompose, flatten, partial, take
from time import time
from ..nodes import  Media, Geotag
from .common import accepts, get_cycled_api


def tap(x, fun):
    fun()
    return x


@accepts(Geotag)
def geotag_feed(bot, nodes, amount, args) -> List[Media]:


    _medias = rcompose(
        lambda tag: tag.id if tag.id else tag.get_id(bot),
        # lambda x: tap(x, lambda: print(bot.last)),
        lambda id: get_feed(id, bot=bot, amount=amount),
    )


    pack_media = rcompose(
        lambda data: Media(id=data['pk'], data=data)
    )

    result = (pack_media(item) for user in nodes for item in _medias(user))
    result = (node for node in result if bot.suitable(node))
    result = take(amount, result)

    return result, bot.last




def get_feed(geotag_id, bot , amount) -> List[Media]:
    return get_cycled_api(bot, bot.api.get_location_feed, geotag_id, 'items', amount)
