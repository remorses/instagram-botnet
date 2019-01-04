
from typing import List
from funcy import  rcompose, flatten, partial, autocurry, fallback, cat, print_calls
from itertools import islice
from ..nodes import User, Media
from .common import accepts, get_cycled_api

@accepts(User)
def user_feed(bot, nodes, amount, args) -> List[Media]:


    get_items = rcompose(
        lambda user: user.get_id(bot) if not user.id else user.id,
        lambda id: get_last_user_feed(id, bot=bot, amount=amount),
    )

    pack_media = lambda data: Media(id=data['pk'], data=data)

    result = (pack_media(item) for user in nodes for item in get_items(user))

    result = (node for node in result if bot.suitable(node))

    result = islice(result, amount)

    return result, bot.last




def get_last_user_feed(id, bot, amount, min_timestamp=None):
    return get_cycled_api(bot, bot.api.get_user_feed, id, 'items', amount)
