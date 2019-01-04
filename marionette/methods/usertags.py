from funcy import rcompose, take
from itertools import islice
from ..nodes import User, Media
from .common import accepts


@accepts(Media)
def usertags(bot, nodes, amount, args) -> User:


    result = (tag for media in nodes for tag in media.usertags(bot))
    result = (user for user in result if bot.suitable(user))
    result = take(amount, result)

    return result, bot.last
