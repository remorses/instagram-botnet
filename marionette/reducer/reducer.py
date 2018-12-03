from functools import reduce
from threading import Thread
from .actions import Action
from .state import State
from ..methods import methods


class Reducer(Thread):

    def __init__(self, state, actions):
        Thread.__init__(self)
        self.logger = state.bot.logger
        self.actions = actions
        self.state = state
        self.result = {}

    def run(self):
        self.logger.info('reducing...')
        self.result = reduce(_reducer, self.actions, self.state)


def _reducer(state: State, action: Action):

    nodes = state.target_nodes
    bot = state.bot
    errors = state.errors

    type = action.type
    amount = action.amount
    args = action.args

    if errors:
        bot.logger.error('trying to solve errors: {}'.format(errors))
        # send_bot_to_phone_verifier
        # change_bot_if_neccessary
        # resolve_captcha_if_necessary
        # sleep_more
        # remove_bot_if_broken

    # try:
    method = methods.get(type, None)
    if not method:
        raise Exception('can\'t find method {}'.format(type))

    next_nodes = method(bot, nodes, amount, args)

    # except Exception as exc:
    #     bot.logger.error('error in method {}: {}'.format(type, exc))
    #     return State(target_nodes=nodes, bot=bot, errors=errors + [exc])

    return State(target_nodes=next_nodes, bot=bot, errors=errors)
