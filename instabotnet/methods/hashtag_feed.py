from typing import List
from funcy import  rcompose, mapcat
from ..nodes import  Media, Hashtag
from .common import accepts, cycled_api_call

@accepts(Hashtag)
def hashtag_feed(bot, nodes,  args) -> List[Media]:
    amount = args.get('amount')

    pack_media = lambda data: Media(id=data['pk'], data=data)

    process = rcompose(
        lambda tag: tag.name,
        # lambda x: tap(x, lambda: print(bot.last)),
        lambda id: cycled_api_call(amount, bot, bot.api.get_hashtag_feed, id, 'items'),
        lambda items: map(pack_media, items),
    )

    result = mapcat(process, nodes)

    return result, bot.last
