from funcy import rcompose, take
import random
from ..nodes import Node
from .common import accepts


@accepts(Node)
def shuffle(bot, nodes,  args) -> Node:

    amount = args.get('amount')
    if amount:
        nodes = take(amount, nodes)
        nodes = random.sample(nodes, k=amount)
    else:
        nodes = list(nodes)
        nodes = random.sample(nodes, k=len(nodes))

    return nodes, bot.last
