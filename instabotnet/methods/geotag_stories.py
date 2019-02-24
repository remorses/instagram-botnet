
from typing import List
from funcy import  rcompose, mapcat

from ..nodes import Story, Geotag
from .common import decorate





@decorate(accepts=Geotag, returns=Story)
def geotag_stories(bot, nodes,  args) -> List[Story]:

    amount = args.get('amount')
    pack_story = lambda data: Story(id=data['pk'], data=data)
    # unmasked = lambda: unmask(bot.last)
    # log_unmasked = lambda: bot.logger.warn(unmasked())
    # bot.logger.warn([x for x in nodes])


    process = rcompose(
        lambda tag: tag.id,
        # lambda id: tap(id, lambda: bot.api.get_user_stories(id)),
        # lambda x: tap(x, lambda: print(x)),
        lambda id: get_stories(bot, id),
        # lambda x: tap(x, lambda: print(x)),
        lambda gen: map(pack_story, gen)
    )

    stories = mapcat(process, nodes)

    return stories, {}

def get_stories(bot, user_id, amount,):
    count = 0
    data = bot.api.feed_location(user_id)
    if 'reel' in data:
        # if data.get('items'):
        #     yield from data['items']
            
        if data.get('story', {}).get('items'):
            yield from data['story']['items']
        
        else:
            yield from []
        # elif data.get('ranked_items'):
        #     yield from data['ranked_items']
    else:
        yield from []
