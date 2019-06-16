from typing import List
from ..bot import Bot
from funcy import  rcompose, mapcat
from ..nodes import  Media, Hashtag, Story
from .common import decorate, cycled_api_call



@decorate(accepts=Hashtag, returns=Media)
def hashtag_stories(bot: Bot, nodes,  args) -> List[Media]:
    amount = args.get('amount') or 1

    pack_story = lambda data: Story(**data)

    process = rcompose(
        lambda tag: tag.name,
        # lambda x: tap(x, lambda: print(bot.last)),
        lambda id: cycled_api_call(amount, bot, bot.api.feed_tag, id, ['story', 'items']),
        lambda items: map(pack_story, items),
    )

    result = mapcat(process, nodes)

    return result, {}
