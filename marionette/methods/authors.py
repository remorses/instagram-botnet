from ..nodes import User, Media
from .common import accepts


@accepts(Media)
def authors(bot, nodes, amount, args):

    nodes = bot.filter(nodes)

    # bot.logger.warn('nodes: ' +  str(nodes))

    ids = [node.id if node.id else get_id(bot, node) for node in nodes]

    _authors = [get_author(bot, id) for id in ids]

    return _authors, bot.last


def get_author(bot, id):
    bot.api.media_info(id)
    data = bot.last["items"][0]["user"]
    id = data["pk"]
    username = data["username"]
    return User(id=id, username=username, data=data)


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
