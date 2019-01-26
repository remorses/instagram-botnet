from funcy import rcompose, take, filter as _filter
from itertools import islice
from ..make_predicate import make_predicate
from ..nodes import Node
from .common import accepts


@accepts(Node)
def filter(bot, nodes,  args) -> Node:

    if args:
        predicate = make_predicate(args, bot)
        nodes = _filter(predicate, nodes)
    else:
        nodes = bot.filter(nodes)


    return nodes, bot.last
