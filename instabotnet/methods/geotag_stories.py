
from typing import List
from funcy import  rcompose, mapcat
from itertools import islice
from ..bot import Bot
from ..nodes import  Story, Geotag
from .common import cycled_api_call, decorate, tap




@decorate(accepts=Geotag, returns=Story)
def geotag_stories(bot: Bot, nodes,  args) -> List[Story]:

    pack_story = lambda data: Story(**data)
    amount = args.get('amount') or 1

    process = rcompose(
        lambda tag: tag.id,
        # lambda x: tap(x, lambda: print(x)),
        lambda id: cycled_api_call(amount, bot, bot.api.location_stories, id, ( 'story', 'items')),
        # lambda x: tap(x, lambda: print(next(x))),
        # lambda gen: islice(gen, amount),
        lambda items: map(pack_story, items),
    )

    result = mapcat(process, nodes)

    return result, {}
