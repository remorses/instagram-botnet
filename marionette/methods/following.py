
from typing import List
from .nodes import User, Media


def following(bot, nodes, amount, args) -> List[User]:

    result = []

    def _following(node) -> List[User]:
            return [User(id=item['pk']) for item in bot.api.get_total_followings(node.id, amount)]

    for node in nodes:

            if isinstance(node, User):
                        result += _following(node)

            elif isinstance(node, str):
                        user = User(username=node)
                        result += _following(user)

    return [users for users in result][::-1] if result else []
