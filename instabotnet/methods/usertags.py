from funcy import mapcat
from typing import List
from ..nodes import User, Media
from .common import decorate





@decorate(accepts=Media, returns=User)
def usertags(bot, nodes,  args) -> List[User]:

    process = lambda media: media.get_usertags(bot)
    result = mapcat(process, nodes)

    return result, {}
