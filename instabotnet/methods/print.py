from .common import decorate
from ..nodes import Node, node_classes

from .common import dotdict
from ..bot import Bot
from funcy import ignore
import json
from itertools import islice
from colorama import init, Fore




@decorate(accepts=(*node_classes.values(),), returns=Node)
def _print(bot: Bot, nodes,  args):

    expr = args['expr']
    def process(node):
        """
        model:
            name:      x.full_name
            id:        x.pk
            followers: x.followers_count
        """
        value = evaluate(expr, node, bot=bot)

        init()
        print()
        print(Fore.CYAN + json.dumps(value, indent=4))
        print()
        return node

    nodes = map(process, nodes)

    return nodes, {}



def evaluate(expr, node, bot):
    x = node
    return xeval(expr, x)


def xeval(expr, x):
    try:
        return eval(expr, dotdict(x=x))

    except (KeyError, AttributeError):
        return None
