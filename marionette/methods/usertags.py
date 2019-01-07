from funcy import rcompose
from typing import List
from ..nodes import User, Media
from .common import accepts


@accepts(Media)
def usertags(bot, nodes,  args) -> List[User]:

    process = lambda media: media.get_usertags(bot)
    result = map(process, nodes)

    return result, bot.last
