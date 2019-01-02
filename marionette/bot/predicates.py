
from ..nodes import Media, User

def not_in_cache(bot, node):
    if isinstance(node, Media):
        if bot.cache['liked'].find_one(identifier=node.id):
            return False
        elif bot.cache['commented'].find_one(identifier=node.id):
            return False
        elif bot.cache['reported'].find_one(identifier=node.id):
            return False
        else:
            return True
    elif isinstance(node, User):
        if bot.cache['followed'].find_one(identifier=node.id):
            return False
        elif bot.cache['blocked'].find_one(identifier=node.id):
            return False
        elif bot.cache['messaged'].find_one(identifier=node.id):
            return False
        else:
            return True
    else:
        return False
