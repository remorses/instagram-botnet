from typing import List
from .nodes import User, Media


def authors(bot, nodes, amount, args) -> List[User]:

    nodes = bot.filter(nodes)

    authors = []

    for node in nodes:

        if isinstance(node, Media):
            authors += [_author(bot, node)]

        elif isinstance(node, str):
            media = Media(url=node)
            authors += [_author(bot, media)]
        else:
            raise Exception('cannot get autor from {}'.format(node))

    return authors


def _author(bot, media):
    bot.api.media_info(media.id)
    data = bot.api.last_json["items"][0]["user"]
    id = data["pk"]
    return User(id=id, data=data)
