from .common import decorate
from ..nodes import Node, User, Media, Story, Geotag, Hashtag

from .common import today, tap, dotdict
from ..bot import Bot
from funcy import mapcat
import time



@decorate(accepts=Node, returns=Node)
def return(bot: Bot, nodes,  args):

    try:
        max = float(args['max']) if 'max' in args else float('inf')
        model = args['model']

    except:
        bot.logger.error('please add all necessary args, {} isn\'t enought'.format(args))
        return [], {}


    count = 0

    def increment():
        nonlocal count
        count += 1



    def process(node):
        """
        model:
            name:      x.full_name
            id:        x.pk
            followers: x.followers_count
        """
        insertion = dotdict()
        for name, expr in model.items():
            insertion[name] = evaluate(expr, node, bot=bot)

        if count <= max:
            bot.logger.info('scraped node {} '.format(node, ))
            increment()
            yield node

        else:
             return


    nodes = mapcat(process, nodes)


    return nodes, {}



def evaluate(expr, node, bot):
    x = node._data or node.get_data(bot)
    x = dotdict(**x)
    value = xeval(expr, x)
    if not value:
        x = node.get_data(bot)
        x = dotdict(**x)
        return xeval(expr, x)
    else:
        return value

def xeval(expr, x):
    try:
        return eval(expr, dict(x=x,
            User=User,
            Story=Story,
            Media=Media,
            Hashtag=Hashtag,
            Geotag=Geotag
        ))

    except (KeyError, AttributeError):
        return None
