from typing import List
from funcy import  rcompose, raiser, ignore
from operator import itemgetter, itemsetter
import time
from .common import accepts, today, tap
from ..nodes import Node, User, Arg




@accepts(Arg)
def set_profile(bot, nodes,  args):

    pick = lambda key: ignore((KeyError, AttributeError), None)(itemgetter(key)(args))


    mode = pick('mode')
    edits = {
            'url': pick('external_url'),
            'phone': pick('phone_number'),
            'username': pick('username'),
            'first_name': pick('full_name'),
            'biography': pick('biography'),
            'email': pick('email'),
            'gender': pick('gender'),
    }

    if mode:
        if mode == 'public':
            bot.api.set_public_account()
        elif mode == 'private':
            bot.api.set_private_account()
        else:
            bot.logger.error('{} is not either "public" or "private"'.format(mode))

    # TODO set default values in edits
    if any([value for value in edits.values()]):
        edits = {key: value for key, value in edits.items() if value}
        bot.api.edit_profile(**edits)

    return [], bot.last
