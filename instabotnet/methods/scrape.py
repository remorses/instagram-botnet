from .common import decorate
from ..nodes import Node, node_classes

from .common import dotdict
from ..bot import Bot
from funcy import mapcat



@decorate(accepts=(*node_classes.values(),), returns=Node)
def scrape(bot: Bot, nodes,  args):

    try:
        max = float(args['max']) if 'max' in args else float('inf')
        key = args.get('key', 'data')
        model = args['model']

    except:
        bot.logger.error('please add all necessary args, {} isn\'t enought'.format(args))
        return [], {}


    count = 0

    def increment():
        nonlocal count
        count += 1

    data = []

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

        data.append(insertion)
        bot.logger.info('scraped node {} '.format(node, ))

        if count <= max:

            increment()
            yield node

        else:
             return

    nodes = mapcat(process, nodes)

    return nodes, {key: data}



def evaluate(expr, node, bot):
    x = node
    return xeval(expr, x)


def xeval(expr, x):
    try:
        return eval(expr, dict(x=x,
            # User=User,
            # Story=Story,
            # Media=Media,
            # Hashtag=Hashtag,
            # Geotag=Geotag
        ))

    except (KeyError, AttributeError):
        return None
