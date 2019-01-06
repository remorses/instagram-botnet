from funcy import rcompose, take
from itertools import islice
from ..nodes import User, Media
from .common import accepts


@accepts(Media)
def usertags(bot, nodes,  args) -> User:


    result = (tag for media in nodes for tag in media.get_usertags(bot))
    # result = (user for user in result if bot.suitable(user))
    result = (user for user in result if user)


    return result, bot.last
