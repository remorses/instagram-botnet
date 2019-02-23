
from typing import List
from funcy import  rcompose, mapcat
from ..nodes import User, Media
from .common import cycled_api_call, decorate




@decorate(accepts=User, returns=Media)
def user_feed(bot, nodes,  args) -> List[Media]:
    try:
        amount = args.get('amount')

        pack_media = lambda data: Media(id=data['pk'], data=data)

        process = rcompose(
            lambda user: user.id if user.id else user.get_id(bot),
            lambda id: cycled_api_call(amount, bot, bot.api.username_feed, id, 'items'),
            lambda items: map(pack_media, items),
            # lambda x: tap(x, lambda: print(x)),

        )

        result = mapcat(process, nodes)

        return result, {}
    except:
        import traceback
        traceback.print_exc()