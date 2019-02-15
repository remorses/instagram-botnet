from funcy import  ignore
from functools import reduce
import time
import traceback

from .bot import Bot
from .methods import methods
from .threads import Thread

class Dont_retry(Exception):
    """
    this exception doesn't cause a retry of the edge method when it is raised.
    Useful when a method is not found in the methods object,
    because it would be just a waste of time to retry.
    """
    pass

class Reducer(Thread):

    def __init__(self, state, edges, name=None):
        super().__init__(name=state['bot'].username)
        self.name = state['bot'].username
        self.logger = state['bot'].logger
        self.edges = edges
        self.state = state



    def run(self):
        get_name = lambda: self.edges[0]['name']
        name = ignore((KeyError, AttributeError), 'unnamed')(get_name)()
        self.logger.debug('reducer beginning {} action'.format(name))
        last_state = reduce(_reducer, self.edges, self.state)
        super().set_data(last_state['data'])
        return




def _reducer(state: dict, edge: dict):

    nodes = state['nodes']
    bot: Bot = state['bot']
    errors = state['errors']
    data = state['data']

    type = edge['type']
    args = edge['args']

    if len(errors) > 1:
        # tried multiple times
        bot.logger.error('trying to solve errors: {}, bot: {}'.format(errors, bot))
        # send_bot_to_phone_verifier
        # change_bot_if_neccessary
        # resolve_captcha_if_necessary
        # sleep_more
        # remove_bot_if_broken

    try:

        # if not nodes:
        #     raise Dont_retry('no nodes, {}'.format(nodes))

        method = methods.get(type, None)

        if not method:
            raise Dont_retry('can\'t find method {}'.format(type))

        # bot.logger.debug('reducing nodes %s' % list(nodes))

        next_nodes, next_data = method(bot, nodes,  args)

        # bot.logger.info('{} did success on {}'.format(type, nodes))
        # bot.logger.debug('{} returned {}'.format(type, next_nodes))

        next_data = merge(data, {'__{}__'.format(type): next_data})

        # secs = bot.delay[type] if type in bot.delay else bot.delay['usual']
        # time.sleep(secs)

    except Dont_retry as exc:
        bot.logger.error('error reducing edge {}: \"{}\" {}'.format(type, exc.__class__.__name__, exc))
        return dict(nodes=[], bot=bot, errors=errors + [exc], data=data)

    except Exception as exc:
        bot.logger.error('error reducing edge {}: \"{}\" \n {}'.format(
            type,
            exc.__class__.__name__,
            '\n'.join(traceback.format_exc().split('\n')[5:])))
        bot.sleep('error')

        errored_state = merge(state, dict(errors=errors + [exc]))
        return _reducer(errored_state, edge)

    else:
        # all is right, no exceptions
        return dict(nodes=next_nodes, bot=bot, errors=[], data=next_data)


def merge(a, b):
    return { key: val for (key, val) in [*a.items(), *b.items()]}
