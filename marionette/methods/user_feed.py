
from typing import List
from .nodes import User, Media


def user_feed(bot, nodes, amount, args) -> List[Media]:

    result = []

    for node in nodes:

        if isinstance(node, User):
                    result += _feed(bot, node, amount)

        elif isinstance(node, str):
                    user = User(username=node)
                    result += _feed(bot, user, amount)
        else:
            raise Exception

    return result


def _feed(bot, node, amount) -> List[Media]:
    return [User(id=item['pk']) for item in bot.api.get_user_feed(node.id)][:amount]
