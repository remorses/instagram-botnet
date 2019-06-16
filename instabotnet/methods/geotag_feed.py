
from typing import List
from funcy import  rcompose, mapcat
from itertools import islice
from ..bot import Bot
from ..nodes import  Media, Geotag
from .common import cycled_api_call, decorate, tap




@decorate(accepts=Geotag, returns=Media)
def geotag_feed(bot: Bot, nodes,  args) -> List[Media]:

    pack_media = lambda data: Media(**data['media'])
    amount = args.get('amount') or 1
    ordering = args.get('ordering', 'ranked')

    process = rcompose(
        lambda tag: tag.id,
        # lambda x: tap(x, lambda: print(x)),
        lambda id: cycled_api_call(None, bot, bot.api.location_section, dict(location_id=id, tab=ordering), ( 'sections',)),
        # lambda x: tap(x, lambda: print(next(x))),
        lambda gen: mapcat(lambda data: data['layout_content']['medias'], gen),
        lambda gen: islice(gen, amount),
        lambda items: map(pack_media, items),
    )

    result = mapcat(process, nodes)

    return result, {}
