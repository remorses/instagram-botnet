from funcy import wraps, autocurry
from datetime import datetime
from time import time
from typing import List
from ..nodes import Node


def accepts(Class):

    def _accepts(original):

        @wraps(original)
        def enhanced(bot, nodes, amount, args, *others, **kwrgs):

            # print('nodes in accepts for {}: {}'.format(original.__name__, nodes))

            if any([not isinstance(node, Class) for node in nodes]):
                raise Exception(
                    'nodes like {} aren\'t instance of {}'.format(nodes[0], Class.__name__))

            result = original(bot, nodes, amount, args, *others, **kwrgs)

            return result

        enhanced.accepts = Class

        return enhanced

    return _accepts

# @autocurry
def get_user_id(node, bot):
    if node.id:
        return node.id
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



def today():
    return datetime.now().strftime("%Y-%m-%d")

def parse_date(date):
    return datetime.strptime(date, "%Y-%m-%d" )





def get_cycled_api(bot, api_method, api_argument, key, amount, ) -> List[Node]:

    next_max_id = ''
    sleep_track = 0
    done = 0

    while True:
        bot.logger.info('new get cycle with %s' % api_method.__name__)
        try:
            api_method(api_argument, max_id=next_max_id)
            items = bot.last[key] if key in bot.last else []

            if 'next_max_id' not in bot.last:
                yield from items
                done += len(items)
                return

            elif "more_available" in bot.last and not bot.last["more_available"]:
                yield from items
                done += len(items)
                return

            elif "big_list" in bot.last and not bot.last['big_list']:
                yield from items
                done += len(items)
                return

            elif (done + len(items)) >= amount:
                yield from items[:(amount - done)]
                done += len(items)
                return

            else:
                yield from items
                done += len(items)

        except Exception as exc:
            bot.logger.error('exception in get_cycled_api: {}'.format(exc))
            return

        if sleep_track > 2:
            bot.logger.debug('sleeping some time while getting')
            time.sleep(bot.delay['getter'])
            sleep_track = 0

        next_max_id = bot.last.get("next_max_id", "")
        sleep_track += 1
