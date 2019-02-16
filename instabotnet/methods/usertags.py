from funcy import rcompose, mapcat
from typing import List
from ..nodes import User, Media
from .common import accepts


@accepts(Media)
def usertags(bot, nodes,  args) -> List[User]:

    process = lambda media: media.get_usertags(bot)
    result = mapcat(process, nodes)

    return result, {}
