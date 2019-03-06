from typing import List
from funcy import  rcompose, mapcat
from ..bot import Bot
from ..nodes import  Media, Hashtag
from .common import decorate, cycled_api_call



@decorate(accepts=Hashtag, returns=Media)
def hashtag_feed(bot: Bot, nodes,  args) -> List[Media]:
    amount = args.get('amount') or 1

    pack_media = lambda data: Media(id=data['pk'], data=data)

    process = rcompose(
        lambda tag: tag.name,
        # lambda x: tap(x, lambda: print(bot.last)),
        lambda name: cycled_api_call(amount, bot, bot.api.feed_tag, (name,), 'items'),
        lambda items: map(pack_media, items),
    )

    result = mapcat(process, nodes)

    return result, {}
