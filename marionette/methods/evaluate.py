from ..nodes import Node
from .common import accepts


@accepts(Node)
def evaluate(bot, nodes,  args) -> Node:

    nodes = list(nodes)

    return nodes, bot.last
