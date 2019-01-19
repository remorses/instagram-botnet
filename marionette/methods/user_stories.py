
from typing import List
from funcy import  rcompose, mapcat
import json
from ..debug import unmask
from ..nodes import User, Media, Story
from .common import accepts, cycled_api_call, tap

@accepts(User)
def user_stories(bot, nodes,  args) -> List[Story]:

    pack_story = lambda data: Story()
    unmasked = lambda: unmask(json.dumps(bot.last, indent=4))
    log_unmasked = lambda: bot.logger.warn(unmasked())


    process = rcompose(
        lambda user: user.id if user.id else user.get_id(bot),
        lambda id: tap(id, lambda: bot.api.get_user_reel(id)),
        lambda id: tap(id, log_unmasked),
        lambda id: tap(id, lambda: bot.api.get_user_stories(id)),
        lambda id: tap(id, log_unmasked),
        lambda items: map(pack_story, items),
    )

    stories = map(process, nodes)

    return stories, bot.last
