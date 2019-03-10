from funcy import filter as _filter
from ..make_predicate import make_predicate
from ..nodes import Node, node_classes
from .common import decorate


@decorate(accepts=(*node_classes.values(),), returns=Node)
def filter(bot, nodes,  args) -> Node:

    if args:
        predicate = make_predicate(args, bot)
        nodes = _filter(predicate, nodes)
    else:
        nodes = bot.filter(nodes)


    return nodes, {}
