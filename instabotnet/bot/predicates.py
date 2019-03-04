
from ..nodes import Media, User, Hashtag, Geotag, Node

def not_in_cache(bot, node,table=None, specifier=None,):

    with bot.cache as cache:

        if table and not specifier:
            if cache[table].find_one(identifier=node.pk, ):
                return False
        elif table and specifier:
            if cache[table].find_one(identifier=node.pk,  specifier=specifier):
                return False

        if isinstance(node, Media):
            kwargs = dict(identifier=node.pk, type='media', )
            if specifier: kwargs['specifier'] = specifier

            if cache['liked'].find_one(**kwargs):
                return False
            elif cache['commented'].find_one(**kwargs):
                return False
            elif cache['reported'].find_one(**kwargs):
                return False
            else:
                return True


        elif isinstance(node, User):
            kwargs = dict(identifier=node.pk, type='user', )
            if specifier: kwargs['specifier'] = specifier

            if cache['followed'].find_one(**kwargs):
                return False
            elif cache['blocked'].find_one(**kwargs):
                return False
            elif cache['texted'].find_one(**kwargs):
                return False
            else:
                return True

        elif isinstance(node, Hashtag):
            return True

        elif isinstance(node, Geotag):
            return True

        elif isinstance(node, Node):
            return True

        else:
            return False
