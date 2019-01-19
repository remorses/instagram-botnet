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
        bot.logger.warn('to shuffle the amount of output nodes is needed, you can\'t shuffle a generator')

    return nodes, bot.last
