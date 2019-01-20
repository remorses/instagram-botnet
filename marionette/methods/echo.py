from .common import accepts
from ..nodes import Node, User, Media
from ..debug import unmask
from .common import today, tap, dotdict
from ..bot import Bot
import json
from dataset import connect
from funcy import rcompose, ignore, mapcat
import time



@accepts(Node)
def echo(bot: Bot, nodes,  args):

    try:
        amount = float(args['amount']) if 'amount' in args else 1
        model = args['model']

    except KeyError as exc:
        bot.logger.error('please add all necessary args, {}'.format( exc))
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

        if count <= amount + 1:
            print()
            print(json.dumps(insertion, indent=4))
            print()
            increment()
            return node

        else:
            raise StopIteration

    nodes = mapcat(process, nodes)

    return nodes, bot.last



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
        return eval(expr, dotdict(x=x))

    except (KeyError, AttributeError):
        return None
