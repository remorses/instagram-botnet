from funcy import wraps, autocurry
from datetime import datetime

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
