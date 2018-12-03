from typing import List
from ..nodes import User, Media


def followers(bot, nodes, amount, args) -> List[User]:

    result = []

    def _followers(node) -> List[User]:
            return [User(id=item['pk']) for item in bot.api.get_total_followers(node.id, amount)]

    for node in nodes:

            if isinstance(node, User):
                        result += _followers(node)

            elif isinstance(node, str):
                        user = User(username=node)
                        result += _followers(user)

    return [users for users in result][::-1] if result else []
