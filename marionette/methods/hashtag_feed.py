
from typing import List
from operator import concat
from functools import reduce
from ..nodes import User, Media, Hashtag
from .common import accepts


@accepts(Hashtag)
def hashtag_feed(bot, nodes, amount, args) -> List[Media]:

    result = []

    result = [get_feed(bot, hashtag.name, amount) for hashtag in nodes]

    result = reduce(concat, result, [])

    result = [Media(id=item['pk']) for item in result]

    return result, bot.last


def get_feed(bot, hashtag, amount) -> List[Media]:

    hashtag_feed = []
    next_max_id = ''

    while True:
        bot.api.get_hashtag_feed(hashtag, next_max_id)
        if 'items' not in bot.last:
            return hashtag_feed[:amount]
        items = bot.last['items']
        try:
            hashtag_feed += items
            if not items or len(hashtag_feed) >= amount:
                return hashtag_feed[:amount]
        except Exception:
            return hashtag_feed[:amount]
        next_max_id = bot.last.get("next_max_id", "")
