
from typing import List
from funcy import  rcompose, flatten, partial
from itertools import islice
from time import time
from ..nodes import  Media, Hashtag
from .common import accepts, get_cycled_api

@accepts(Hashtag)
def geotag_feed(bot, nodes, amount, args) -> List[Media]:


    _medias = rcompose(
        lambda tag: tag.id,
        lambda id: get_feed(id, bot=bot, amount=amount),
    )

    pack_media = rcompose(
        lambda data: data['pk'],
        lambda id: Media(id=id)
    )

    result = (pack_media(item) for user in nodes for item in _medias(user))
    result = (node for node in result if bot.suitable(node))
    result = islice(result, amount)

    return result, bot.last




def get_feed(geotag_id, bot , amount) -> List[Media]:
    return get_cycled_api(bot, bot.api.get_location_feed, geotag_id, 'items', amount)
