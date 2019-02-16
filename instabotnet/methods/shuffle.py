from funcy import rcompose, take
import random
from ..nodes import Node
from .common import accepts


@accepts(Node)
def shuffle(bot, nodes,  args) -> Node:

    max = args.get('max') # None works as inf
    batch = args.get('batch', max) # None works as inf
    nodes = take(batch, nodes)
    if max and max <= len(nodes):
        nodes = random.sample(nodes, k=max)
    else:
        nodes = random.sample(nodes, k=len(nodes))


    return nodes, {}
