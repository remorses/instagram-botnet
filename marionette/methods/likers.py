
from typing import List
from funcy import  rcompose, flatten, partial, print_calls
from itertools import islice
from ..nodes import  Media, User
from .common import accepts, cycled_api_call

@accepts(Media)
def likers(bot, nodes,  args) -> List[Media]:
    """
    get at max 1000 likers
    """

    get_items = rcompose(
        lambda media: media.id,
        lambda id: get_likers(id, bot=bot),
    )

    pack_user = lambda data: User(id=data['pk'], username=data['username'], data=data)

    result = (pack_user(item) for media in nodes for item in get_items(media))
    # result = (media for media in result if bot.suitable(media))
    result = (media for media in result if media)


    return result, bot.last




def get_likers(id, bot) -> List[Media]:
    bot.api.get_media_likers(id)
    yield from bot.last['users']
