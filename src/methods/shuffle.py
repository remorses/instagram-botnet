from funcy import rcompose, take
import random
from ..nodes import Node
from .common import accepts


@accepts(Node)
def shuffle(bot, nodes,  args) -> Node:

    amount = args.get('amount')
    if amount:
        nodes = take(amount, nodes)
        if amount <= len(nodes):
            nodes = random.sample(nodes, k=amount)
        else:
            nodes = random.sample(nodes, k=len(nodes))
    else:
        nodes = list(nodes)
        nodes = random.sample(nodes, k=len(nodes))

    return nodes, bot.last
