
from typing import List
from funcy import  rcompose, flatten, partial, autocurry, fallback, cat, print_calls
from ..nodes import User, Media
from .common import accepts, get_user_id

@accepts(User)
def user_feed(bot, nodes, amount, args) -> List[Media]:


    get_items = rcompose(
        lambda user: get_user_id(user, bot=bot) if not user.id else user.id,
        lambda id: get_last_user_feed(id, bot=bot, amount=amount),
    )

    pack_media = rcompose(
        lambda data: data['pk'],
        lambda id: Media(id=id)
    )

    result = (pack_media(item) for user in nodes for item in get_items(user))

    result = list(flatten(result))

    return result, bot.last




def get_last_user_feed(id, bot, amount, min_timestamp=None):

    next_max_id = ''
    done = 0

    while True:

        bot.api.get_user_feed(id, next_max_id, min_timestamp)
        items = bot.last["items"] if 'items' in bot.last else []

        if len(items) <= amount:
            yield from items
            done += len(items)
            return

        elif (done + len(items)) >= amount:
            yield from items[:amount - done]
            done += len(items)
            return

        elif not bot.last.get("more_available"):
            yield from items
            return

        else:
            yield from items
            done += len(items)

        next_max_id = bot.last.get("next_max_id", "")
