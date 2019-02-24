from funcy import mapcat
from ..nodes import User, Media
from .common import decorate


@decorate(accepts=Media, returns=User)
def author(bot, nodes,  args):


    process = rcompose(
        lambda media: media._data['user'],
        lambda data: User(data=data),
    )
    
    result = mapcat(process, nodes)

    return result, {}


 