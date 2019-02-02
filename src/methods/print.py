from .common import accepts
from ..nodes import Node, User, Media

from .common import today, tap, dotdict
from ..bot import Bot
import json
from dataset import connect
from funcy import rcompose, ignore, mapcat
from itertools import islice
from colorama import init, Fore
import time



@accepts(Node)
def _print(bot: Bot, nodes,  args):

    try:
        max = float(args['max']) if 'max' in args else 1
        model = args['model']

    except KeyError as exc:
        bot.logger.error('please add all necessary args, {}'.format( exc))
        return [], {}


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

        init()
        print()
        print(Fore.CYAN + json.dumps(insertion, indent=4))
        print()
        return node

    max = ignore(OverflowError, None)(lambda: int(max))()
    nodes = map(process, islice(nodes, max))

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
