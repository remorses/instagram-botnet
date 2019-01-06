
from typing import List
from funcy import  rcompose, flatten, partial, take
from time import time
from ..nodes import  Media, Geotag
from .common import accepts, cycled_api_call


def tap(x, fun):
    fun()
    return x


@accepts(Geotag)
def geotag_feed(bot, nodes,  args) -> List[Media]:


    _medias = rcompose(
        lambda tag: tag.id if tag.id else tag.get_id(bot),
        # lambda x: tap(x, lambda: print(bot.last)),
        lambda id: get_feed(id, bot=bot),
    )


    pack_media = rcompose(
        lambda data: Media(id=data['pk'], data=data)
    )

    result = (pack_media(item) for user in nodes for item in _medias(user))
    # result = (node for node in result if bot.suitable(node))
    result = (node for node in result if node)


    return result, bot.last




def get_feed(geotag_id, bot ) -> List[Media]:
    return cycled_api_call(bot, bot.api.get_location_feed, geotag_id, 'items')
