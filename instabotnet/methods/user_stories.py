
from typing import List
from funcy import  rcompose, mapcat

from ..nodes import Story, User
from .common import decorate





@decorate(accepts=User, returns=Story)
def user_stories(bot, nodes,  args) -> List[Story]:

    amount = args.get('amount')
    pack_story = lambda data: Story(id=data['pk'], data=data)
    # unmasked = lambda: unmask(bot.last)
    # log_unmasked = lambda: bot.logger.warn(unmasked())
    # bot.logger.warn([x for x in nodes])


    process = rcompose(
        lambda user: user.id if user.id else user.get_id(bot),
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
    data = bot.api.user_story_feed(user_id)
    if 'reel' in data:
        yield from data['reel']['items'][:amount]
    else:
        yield from []
