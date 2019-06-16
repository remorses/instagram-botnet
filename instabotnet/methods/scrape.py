from .common import decorate
from ..nodes import Node, node_classes
import json
from .common import dotdict
from ..bot import Bot
from funcy import mapcat



@decorate(accepts=(*node_classes.values(),), returns=Node)
def scrape(bot: Bot, nodes,  args):

    try:
        max = float(args['max']) if 'max' in args else float('inf')
        key = args.get('key', 'data')
        model = args['model']

    except Exception:
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
        if isinstance(model, dict):
            insertion = dotdict()
            for name, expr in model.items():
                insertion[name] = evaluate(expr, node, bot=bot)
        elif isinstance(model, str):
            insertion = evaluate(model, node, bot=bot)
        
        # print(json.dumps(insertion, indent=4))

        data.append(insertion)
        bot.logger.info('scraped node {} '.format(node, ))

        if count <= max:
            increment()
            yield node

        else:
             return None

    nodes = mapcat(process, nodes)

    return nodes, {key: data}



def evaluate(expr, node, bot):
    try:
        return eval(expr, dict(x=node,
            # User=User,
            # Story=Story,
            # Media=Media,
            # Hashtag=Hashtag,
            # Geotag=Geotag
        ))

    except (KeyError, AttributeError) as e:
        bot.logger.error(f'error evaluating expression {expr}')
        bot.logger.error(e)
        # bot.logger.error(treaceback.format_exc())
        return None
