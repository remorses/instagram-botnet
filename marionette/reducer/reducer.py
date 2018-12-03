from functools import reduce
from threading import Thread
from .actions import make_actions, Action
from .state import make_state, State
from ..methods import methods


class Reducer(Thread):

    def __init__(self, state, actions):
        self.actions = actions
        self.state = state

    def run(self):
        reduce(_reducer, self.actions, self.state)


def _reducer(state: State, action: Action):
    nodes = state.target_nodes
    bot = state.bot
    errors = state.errors

    if errors:
        pass
        # send_bot_to_phone_verifier
        # change_bot_if_neccessary
        # resolve_captcha_if_necessary
        # sleep_more
        # remove_bot_if_broken

    try:
        method = methods.get(action.type, lambda x: x)
        next_nodes = method(bot, nodes, action.amount, action.args)

    except Exception as exc:
        return State(target_nodes=nodes, bot=bot, errors=errors + [exc])

    return State(target_nodes=next_nodes, bot=bot, errors=errors)
