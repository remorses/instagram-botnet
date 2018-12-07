from typing import List
from functools import reduce
from operator import concat
from random import uniform
import time
from ..bot import Bot
from ..nodes import User, Media
from .common import accepts


@accepts(User)
def followers(bot, nodes, amount, args) -> List[User]:

    result = []

    ids = [id if user.id else get_id(bot, user) for user in nodes]

    result = [get_followers(bot, id, amount) for id in ids]

    result = reduce(concat, result, [])

    result = [User(id=item['pk'], username=item['username']) for item in result]

    return result[::-1], bot.last


def get_id(bot, node):
    if node.username:
        if node.username not in bot.cache.usernames:
            bot.api.search_username(node.username)
            if "user" in bot.api.last_json:
                bot.cache.usernames[node.username] = str(bot.api.last_json["user"]["pk"])
            else:
                return None
        return str(bot.api.last_json["user"]["pk"])
    else:
        raise Exception('username is needed to get the id')


def get_followers(bot: Bot, user_id, total) -> List[User]:

        bot.logger.info('following user_id %s' % user_id)

        sleep_track = 0
        result = []
        next_max_id = ''
        # bot.api.get_username_info(user_id)
        # bot.logger.error(bot.last)
        # username_info = bot.last
        # if "user" in username_info:
        #     total = amount or username_info["user"]['follower_count']
        #     if total > 200000:
        #         bot.logger.warn("Consider temporarily saving the result of this big "
        #               "operation. This will take a while.\n")
        # else:
        #     return False

        while True:
            bot.api.get_user_followers(user_id, next_max_id)
            last_json = bot.last
            try:
                for item in last_json["users"]:
                    result.append(item)
                    sleep_track += 1
                    if sleep_track >= 20000:
                        sleep_time = uniform(120, 180)
                        msg = "\nWaiting {:.2f} min. due to too many requests."
                        print(msg.format(sleep_time / 60))
                        time.sleep(sleep_time)
                        sleep_track = 0
                if not last_json["users"] or len(result) >= total:
                    return result[:total]
            except Exception:
                return result[:total]

            if last_json["big_list"] is False:
                return result[:total]

            next_max_id = last_json.get("next_max_id", "")
