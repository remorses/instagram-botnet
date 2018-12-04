from functools import reduce
from .actions import Action
from .state import State
from ..methods import methods
from ..threads import Thread


class Reducer(Thread):

    def __init__(self, state, actions, name=None):
        super().__init__(name=state.bot.username)
        self.name = state.bot.username
        self.logger = state.bot.logger
        self.actions = actions
        self.state = state

    def run(self):
        self.logger.debug('{} is reducing the {} interaction'.format(
            self.state.bot, self.actions[0].type))
        last_state = reduce(_reducer, self.actions, self.state)
        super().set_data(last_state.data)
        return


def _reducer(state: State, action: Action):

    nodes = state.target_nodes
    bot = state.bot
    errors = state.errors
    data = state.data

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

    try:
        method = methods.get(type, None)

        if not method:
            raise Exception('can\'t find method {}'.format(type))

        next_nodes, next_data = method(bot, nodes, amount, args)

    except Exception as exc:
        bot.logger.error('error in method {}: {}'.format(type, exc))
        return State(target_nodes=nodes, bot=bot, errors=errors + [exc], data=data)

    return State(target_nodes=next_nodes, bot=bot, errors=errors, data=data + [next_data])
