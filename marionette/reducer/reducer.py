from functools import reduce
import time
import traceback
from .actions import Action
from .state import State
from ..bot import Bot
from ..methods import methods
from ..threads import Thread

class Dont_retry(Exception):
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
        last_action = self.actions[-1].type
        self.logger.debug('{} interaction begins'.format( last_action, ))
        last_state = reduce(_reducer, self.actions, self.state)
        super().set_data(last_state.data)
        self.logger.debug('{} interaction ends'.format( last_action,))
        return



def _reducer(state: State, action: Action):

    nodes = state.target_nodes
    bot: Bot = state.bot
    errors = state.errors
    data = state.data

    type = action.type
    amount = action.amount
    args = action.args

    if len(errors) > 1:
        # tried multiple times
        bot.logger.error('trying to solve errors: {}, bot: {}'.format(errors, bot))
        # send_bot_to_phone_verifier
        # change_bot_if_neccessary
        # resolve_captcha_if_necessary
        # sleep_more
        # remove_bot_if_broken

    try:
        nodes = list(nodes)

        if not nodes:
            raise Dont_retry('no nodes, {}'.format(nodes))

        method = methods.get(type, False)

        if not method:
            raise Dont_retry('can\'t find method {}'.format(type))

        next_nodes, next_data = method(bot, nodes, amount, args)

        next_nodes = list(next_nodes)

        bot.logger.info('{} did success on {}'.format(type, nodes))
        bot.logger.debug('{} returned {}'.format(type, next_nodes))

        next_data = merge(data, {'__{}__'.format(type): next_data})

        secs = bot.delay[type] if type in bot.delay else bot.delay['usual']
        time.sleep(secs)

    except Dont_retry as exc:
        bot.logger.error('error reducing action {}: \"{}\" {}'.format(type, exc.__class__.__name__, traceback.format_exc()))
        return State(target_nodes=[], bot=bot, errors=errors + [exc], data=data)

    except Exception as exc:
        bot.logger.error('error reducing action {}: \"{}\" \n {}'.format(type, exc.__class__.__name__, traceback.format_exc()))
        bot.logger.warn('sleeping some time before retrying')
        time.sleep(bot.delay['error'])

        errored_state = merge(state, dict(errors=errors + [exc]))
        return _reducer(errored_state, action)

    else:
        # all is right, no exceptions
        return State(target_nodes=next_nodes, bot=bot, errors=[], data=next_data)


def merge(a, b):
    return { key: val for (key, val) in [*a.items(), *b.items()]}
