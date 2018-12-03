from typing import List
from ..nodes import Node, User, Media


def like(bot, nodes, amount, args):

    nodes = bot.filter(nodes)

    for node in nodes:
        if isinstance(node, Media):
            bot.api.like(node.id)

        else:
            raise Exception('{} isn\' a Media'.format(node))

    return
