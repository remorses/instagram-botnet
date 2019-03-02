
from typing import List
from funcy import  rcompose, mapcat
from ..bot import Bot
from ..nodes import Story, User
from .common import decorate, tap




@decorate(accepts=User, returns=Story)
def user_stories(bot, nodes,  args) -> List[Story]:

    amount = args.get('amount')
    pack_story = lambda data: Story(**data)
    # unmasked = lambda: unmask(bot.last)
    # log_unmasked = lambda: bot.logger.warn(unmasked())
    # bot.logger.warn([x for x in nodes])


    process = rcompose(
        lambda user: user.id,
        # lambda id: tap(id, lambda: bot.api.get_user_stories(id)),
        # lambda x: tap(x, lambda: print(x)),
        lambda id: get_stories(bot, id, amount),
        lambda gen: map(pack_story, gen),
        lambda x: tap(x, lambda: print(next(x)._json())),
    )

    stories = mapcat(process, nodes)

    return stories, {}

def get_stories(bot: Bot, user_id, amount,):
    count = 0
    data = bot.api.user_story_feed(user_id)
    # import json
    # print(json.dumps(data['reel']['items'], indent=4))
    if data['reel']:
        yield from data['reel']['items'][:amount]
    else:
        yield from []




schema = """

properties:
  broadcast:
    type: 'null'
  reel:
    properties:
      can_reply:
        type: boolean
      can_reshare:
        type: boolean
      expiring_at:
        type: integer
      has_besties_media:
        type: boolean
      id:
        type: integer
      items:
        type: array
        items:
          $ref: story.yaml
      latest_reel_media:
        type: integer
      media_count:
        type: integer
      prefetch_count:
        type: integer
      reel_type:
        type: string
      seen:
        type: integer
      user:
        $ref: user.yaml
    required:
      - can_reply
      - can_reshare
      - expiring_at
      - items
      - media_count
      - prefetch_count
      - reel_type
      - seen
      - user
    type: object
  status:
    type: string
required:
  - reel
  - status
type: object


"""
