from typing import List
from funcy import  rcompose, raiser, ignore
from operator import itemgetter
import time

from .common import accepts, today, tap
from ..nodes import Node, User, Arg




@accepts(Arg)
def set_profile(bot, nodes,  args):


    @ignore((KeyError, AttributeError), None)
    def pick(key):
        return args[key]

    mode = pick('mode')
    edits = {
        'external_url': pick('external_url'),
        'phone_number': pick('phone_number'),
        'username': pick('username'),
        'full_name': pick('full_name'),
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
        bot.api.get_profile_data()

        previous_values = bot.last['user']
        new_values = {key: value for key, value in edits.items() if value}

        edits = {**previous_values, **new_values}
        bot.api.edit_profile(**edits)

    bot.logger.info('changed profile values')

    return [], bot.last
