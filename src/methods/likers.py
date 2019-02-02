
from typing import List
from funcy import  rcompose, mapcat
from ..nodes import  Media, User
from .common import accepts

@accepts(Media)
def likers(bot, nodes,  args) -> List[Media]:

    pack_user = lambda item: User(id=item['pk'], username=item['username'], data=item)
    amount = args.get('amount')

    process = rcompose(
            lambda media: media.id if media.id else media.get_id(bot),
            lambda id: get_likers(id, bot, amount),
            lambda gen: map(pack_user, gen)
        )

    result = mapcat(process, nodes)


    return result, bot.last





def get_likers(id, bot, amount):
    bot.api.get_media_likers(id)
    if 'users' in bot.last:
        yield from bot.last['users'][:amount]
    else:
        yield from []
