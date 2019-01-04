
from typing import List
from funcy import  rcompose, flatten, partial
from itertools import islice
from time import time
from ..nodes import  Media, Hashtag
from .common import accepts, get_cycled_api

@accepts(Hashtag)
def hashtag_feed(bot, nodes, amount, args) -> List[Media]:


    get_items = rcompose(
        lambda tag: tag.name,
        lambda name: get_feed(name, bot=bot, amount=amount),
    )

    pack_media = lambda data: Media(id=data['pk'], data=data)


    result = (pack_media(item) for user in nodes for item in get_items(user))
    result = (node for node in result if bot.suitable(node))
    result = islice(result, amount)

    return result, bot.last




def get_feed(hashtag, bot , amount) -> List[Media]:
    return get_cycled_api(bot, bot.api.get_hashtag_feed, hashtag, 'items', amount)
