from ..nodes import Node
from .common import accepts


@accepts(Node)
def evaluate(bot, nodes,  args) -> Node:

    nodes = list(nodes)
    # bot.logger.warn(nodes[:3])

    return nodes, bot.last
