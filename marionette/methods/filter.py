from funcy import rcompose, take
from itertools import islice
from ..nodes import Node
from .common import accepts


@accepts(Node)
def filter(bot, nodes,  args) -> Node:

    nodes = bot.filter(nodes)

    return nodes, bot.last
