
from typing import List
from ..nodes import User, Media
from .common import accepts


@accepts(User)
def following(bot, nodes, amount, args) -> List[User]:

    data = []
    users = []

    for node in nodes:

        data += get_data(bot, node)
        users += [User(id=item['pk'], username=item['username']) for item in data]


    return users[::-1], data


def get_data(bot, node, amount) -> List[User]:
        return [item for item in bot.api.get_total_followings(node.id, amount)]
