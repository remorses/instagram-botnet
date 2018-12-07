
from typing import List
from functools import reduce
from operator import concat
from ..nodes import User, Media
from .common import accepts, get_user_id


@accepts(User)
def user_feed(bot, nodes, amount, args) -> List[Media]:

    result = []

    ids = [get_user_id(bot, user) for user in nodes]

    result = [get_last_user_feed(bot, id, amount) for id in ids]

    result = reduce(concat, result, [])

    result = [Media(id=item['pk']) for item in result]

    return result, bot.last





def get_last_user_feed(bot, user_id, amount, min_timestamp=None):
    user_feed = []
    next_max_id = ''

    while True:
        if len(user_feed) >= amount:
            return user_feed[:amount]
        bot.api.get_user_feed(user_id, next_max_id, min_timestamp)
        last_json = bot.last
        if 'items' not in last_json:
            return user_feed[:amount] if len(user_feed) >= amount else user_feed
        user_feed += last_json["items"]
        if not last_json.get("more_available"):
            return user_feed[:amount] if len(user_feed) >= amount else user_feed

        next_max_id = last_json.get("next_max_id", "")
