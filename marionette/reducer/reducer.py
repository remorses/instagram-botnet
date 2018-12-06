from functools import reduce
import time
from .actions import Action
from .state import State
from ..bot import Bot
from ..methods import methods
from ..threads import Thread

class Dont_retry():
    """
    this exception doesn't cause a retry of the action method when it is raised.
    Useful when a method is not found in the methods object,
    because it would be just a waste of time to retry.
    """
    pass

class Reducer(Thread):

    def __init__(self, state, actions, name=None):
        super().__init__(name=state.bot.username)
        self.name = state.bot.username
        self.logger = state.bot.logger
        self.actions = actions
        self.state = state


    def run(self):
        self.logger.debug('{} is reducing the {} interaction'.format(self.state.bot, self.actions[0].type))
        last_state = reduce(_reducer, self.actions, self.state)
        super().set_data(last_state.data)
        return



def _reducer(state: State, action: Action):

    nodes = state.target_nodes
    bot: Bot = state.bot
    errors = state.errors
    data = state.data

    type = action.type
    amount = action.amount
    args = action.args

    if errors > 1:
        # tried multiple times
        bot.logger.error('trying to solve errors: {}'.format(errors))
        # send_bot_to_phone_verifier
        # change_bot_if_neccessary
        # resolve_captcha_if_necessary
        # sleep_more
        # remove_bot_if_broken

    try:
        method = methods.get(type, None)

        if not method:
            raise Dont_retry('can\'t find method {}'.format(type))

        next_nodes, next_data = method(bot, nodes, amount, args)
        next_data = merge(data, {'__{}__'.format(type): next_data})

    except Dont_retry as exc:
        bot.logger.warn('there was an exception during execution of {}: {}'.format(type, exc.message))
        bot.logger.warn('sleeping some time before retrying')
        return State(target_nodes=next_nodes, bot=bot, errors=errors + [exc], data=next_data)

    except Exception as exc:
        bot.logger.warn('there was an exception during execution of {}: {}'.format(type, exc.message))
        bot.logger.warn('sleeping some time before retrying')
        time.wait(bot.delay['error'])

        errored_state = merge(state, dict(errors=errors + [exc]))
        return _reducer(errored_state, action)

    else:
        return State(target_nodes=next_nodes, bot=bot, errors=[], data=next_data)


def merge(a, b):
    return { key: val for (key, val) in [*a.items(), *b.items()]}
