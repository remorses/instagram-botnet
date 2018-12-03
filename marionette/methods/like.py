from typing import List
from ..nodes import Node, User, Media


def like(bot, nodes, amount, args) -> List[User]:

    nodes = bot.filter(nodes)

    for node in nodes:

        if isinstance(node, Media):
            pass

        else:
            raise Exception('{} isn\' a Media'.format(node))

    return
