
from typing import List
from funcy import  rcompose, flatten, partial, autocurry, fallback, cat, print_calls
from itertools import islice
from ..nodes import User, Media
from .common import accepts, cycled_api_call

@accepts(User)
def user_feed(bot, nodes,  args) -> List[Media]:


    get_items = rcompose(
        lambda user: user.get_id(bot) if not user.id else user.id,
        lambda id: get_last_user_feed(id, bot=bot),
    )

    pack_media = lambda data: Media(id=data['pk'], data=data)

    result = (pack_media(item) for user in nodes for item in get_items(user))

    # result = (node for node in result if bot.suitable(node))
    result = (node for node in result if node)



    return result, bot.last




def get_last_user_feed(id, bot,  min_timestamp=None):
    return cycled_api_call(bot, bot.api.get_user_feed, id, 'items')
