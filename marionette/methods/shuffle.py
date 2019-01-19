from funcy import rcompose
import random
from ..nodes import Node
from .common import accepts


@accepts(Node)
def shuffle(bot, nodes,  args) -> Node:

    amount = args.get('amount')
    if amount:
        nodes = list(nodes)[:amount]
        nodes = random.shuffle(nodes)
        print(nodes)
    else:
        bot.logger.warn('to shuffle the amount of output nodes is needed, you can\'t shuffle a generator')

    return nodes, bot.last
