
from ..nodes import Media, User, Hashtag, Geotag

def not_in_cache(bot, node):

    with bot.cache as cache:
        if isinstance(node, Media):
            if cache['liked'].find_one(identifier=node.id):
                return False
            elif cache['commented'].find_one(identifier=node.id):
                return False
            elif cache['reported'].find_one(identifier=node.id):
                return False
            else:
                return True


        elif isinstance(node, User):
            if cache['followed'].find_one(identifier=node.id):
                return False
            elif cache['blocked'].find_one(identifier=node.id):
                return False
            elif cache['messaged'].find_one(identifier=node.id):
                return False
            else:
                return True


        elif isinstance(node, Hashtag):
            return True

        elif isinstance(node, Geotag):
            return True

        else:
            return False
