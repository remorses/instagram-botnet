from funcy import rcompose, take
from itertools import islice
from ..nodes import Node
from .common import accepts


@accepts(Node)
def usertags(bot, nodes, amount, args) -> Node:

    nodes = (node for node in nodes if bot.suitable(node))

    return nodes, bot.last
