
from typing import List
from funcy import  rcompose, mapcat
from ..nodes import  Media, Geotag
from .common import accepts, cycled_api_call, tap




@accepts(Geotag)
def geotag_feed(bot, nodes,  args) -> List[Media]:

    pack_media = lambda data: Media(id=data['pk'], data=data)
    amount = args.get('amount')

    process = rcompose(
        lambda tag: tag.id if tag.id else tag.get_id(bot),
        # lambda x: tap(x, lambda: print(bot.last)),
        lambda id: cycled_api_call(amount, bot, bot.api.get_location_feed, id, 'items'),
        lambda items: map(pack_media, items),
    )

    result = mapcat(process, nodes)

    return result, bot.last
