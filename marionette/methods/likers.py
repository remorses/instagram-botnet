
from typing import List
from funcy import  rcompose, flatten, partial, print_calls
from ..nodes import  Media, User
from .common import accepts

@accepts(Media)
def likers(bot, nodes, amount, args) -> List[Media]:
    """
    get at max 1000 likers
    """

    get_items = rcompose(
        lambda media: media.id,
        lambda id: get_likers(id, bot=bot, amount=amount),
    )

    pack_user = lambda data: User(id=data['pk'], username=data['username'])


    result = (pack_user(item) for media in nodes for item in get_items(media))


    return list(result), bot.last




def get_likers(id, bot , amount) -> List[Media]:

    while True:
        try:
            bot.api.get_media_likers(id)
            items = bot.last["users"] if 'users' in bot.last else []

            if len(items) <= amount:
                yield from items
                return

            else:
                yield from items[:amount]
                return


        except Exception:
            return
