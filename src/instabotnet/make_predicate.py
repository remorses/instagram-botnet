from .nodes import Media, User, Geotag, Hashtag, Node
from .bot import Bot
from modeller import Model

def access(node, string, bot: Bot): # attr1.attr2
    obj = node
    for attr in string.split('.'):
        if isinstance(obj, Node) and not attr in obj:
            if isinstance(obj, User):
                data = bot.api.user_info(node.pk)
                data = data['user']
                node.__init__(**data)
            elif isinstance(obj, Media):
                data = bot.api.media_info(node.pk)
                data = data['items'][0]
                node.__init__(**data)
        obj = obj[attr]

    return obj


def make_predicate(script, bot): # TODO this is fucked up
    """
    filter:

        user:
            followers:      x > 50 and x < 1000
            following:      x < 500
            bio:            any(s not in ['porn', 'sex'] for s in x)
            is_private:     x and False
            is_business:    x and False
            is_verified:    x and False

        media:
            likes:          x < 200
            comments:       x < 100
            caption:        any(s not in x for s in ['porn', 'sex'])

        hashtag:
            name:           not in [porn, sex]

        geotag:
            name:           not in {{ cities }}
            lat:            x < 1000 and x > 500
            lng:            x < 1000 and x > 500


    """
    def predicate(node, **kwargs):
        res = True
        for (k, expr) in script.items():
            try:
                val = access(node, k, bot)
                if val is None:
                    bot.logger.error(f'failed access to {k}')
                    continue
                new_res = res and eval(expr, dict(x=val,))
                if res and not new_res:
                    bot.logger.info('{} not suitable for {}'.format(node, expr))
                res = new_res
            except (KeyError, AttributeError) as e:
                bot.logger.error(f'failed to check expression in filter: {e} for {k}')

        return res

    return predicate




