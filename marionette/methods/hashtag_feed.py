
from typing import List
from funcy import  rcompose, flatten, partial
from itertools import islice
from time import time
from ..nodes import  Media, Hashtag
from .common import accepts, cycled_api_call

@accepts(Hashtag)
def hashtag_feed(bot, nodes,  args) -> List[Media]:


    get_items = rcompose(
        lambda tag: tag.name,
        lambda name: get_feed(name, bot=bot),
    )

    pack_media = lambda data: Media(id=data['pk'], data=data)


    result = (pack_media(item) for user in nodes for item in get_items(user))
    result = (node for node in result if node)
    # result = (node for node in result if node)


    return result, bot.last




def get_feed(hashtag, bot ) -> List[Media]:
    return cycled_api_call(bot, bot.api.get_hashtag_feed, hashtag, 'items')
