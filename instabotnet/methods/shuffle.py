from funcy import rcompose, take
import random
from ..nodes import Node
from .common import accepts


@accepts(Node)
def shuffle(bot, nodes,  args) -> Node:

    max = args.get('max') # None works as inf
    if max:
        nodes = take(max, nodes)
        if max <= len(nodes):
            nodes = random.sample(nodes, k=max)
        else:
            nodes = random.sample(nodes, k=len(nodes))
    else:
        nodes = list(nodes)
        nodes = random.sample(nodes, k=len(nodes))

    return nodes, {}
