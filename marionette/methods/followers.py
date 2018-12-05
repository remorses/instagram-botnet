from typing import List
from ..nodes import User, Media


def followers(bot, nodes, amount, args) -> List[User]:

    result = []



    for node in nodes:

            if isinstance(node, User):
                        result += get_followers(node)


    return [users for users in result][::-1] if result else []


def get_followers(bot, node, amount) -> List[User]:
        return [User(id=item['pk']) for item in bot.api.get_total_followers(node.id, amount)]
