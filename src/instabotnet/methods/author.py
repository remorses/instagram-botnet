from funcy import mapcat, rcompose
from ..nodes import User, Media
from .common import decorate


@decorate(accepts=Media, returns=User)
def author(bot, nodes,  args):

    process = rcompose(
        lambda media: media['user'],
        lambda data: User(**data),
    )

    result = map(process, nodes)

    return result, {}
