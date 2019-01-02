from typing import List
from funcy import rcompose
from itertools import islice
from random import uniform
import time
from ..bot import Bot
from ..nodes import User, Media
from .common import accepts


@accepts(User)
def followers(bot, nodes, amount, args) -> List[User]:

    pack_user = lambda item: User(id=item['pk'], username=item['username'])

    _followers = rcompose(
        lambda user: user.id if user.id else user.get_id(bot),
        lambda id: get_followers(bot, id, amount),
    )

    result = (pack_user(item) for node in nodes for item in _followers(node) )
    result = (user for user in result if bot.suitable(user))
    result = islice(result, amount)

    return result, bot.last





def get_followers( bot ,id,  amount) -> List[User]:

    next_max_id = ''
    sleep_track = 0
    done = 0

    while True:
        try:
            bot.api.get_user_followers(id, next_max_id)
            items = bot.last["users"] if 'users' in bot.last else []

            if len(items) <= amount:
                yield from items
                done += len(items)
                return

            elif (done + len(items)) >= amount:
                yield from items[:amount - done]
                done += len(items)
                return

            else:
                yield from items
                done += len(items)

        except Exception:
            return

        if sleep_track > 10:
            bot.logger.debug('sleeping some time while getting followers')
            time.sleep(bot.delay['getter'])
            sleep_track = 0

        next_max_id = bot.last.get("next_max_id", "")
        sleep_track += 1








# def get_followers(bot: Bot, user_id, total) -> List[User]:
#
#
#         sleep_track = 0
#         result = []
#         next_max_id = ''
#         # bot.api.get_username_info(user_id)
#         # bot.logger.error(bot.last)
#         # username_info = bot.last
#         # if "user" in username_info:
#         #     total = amount or username_info["user"]['follower_count']
#         #     if total > 200000:
#         #         bot.logger.warn("Consider temporarily saving the result of this big "
#         #               "operation. This will take a while.\n")
#         # else:
#         #     return False
#
#         while True:
#             bot.api.get_user_followers(user_id, next_max_id)
#             last_json = bot.last
#             try:
#                 for item in last_json["users"]:
#                     result.append(item)
#                     sleep_track += 1
#                     if sleep_track >= 20000:
#                         sleep_time = uniform(120, 180)
#                         msg = "\nWaiting {:.2f} min. due to too many requests."
#                         print(msg.format(sleep_time / 60))
#                         time.sleep(sleep_time)
#                         sleep_track = 0
#                 if not last_json["users"] or len(result) >= total:
#                     return result[:total]
#             except Exception:
#                 return result[:total]
#
#             if last_json["big_list"] is False:
#                 return result[:total]
#
#             next_max_id = last_json.get("next_max_id", "")
