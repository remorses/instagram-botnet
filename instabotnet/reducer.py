
from .support import dotdict, merge
# from .api.exceptions import InstagramApiError
from .api.instagram_private_api.errors import ClientError
from .methods import methods
import traceback

class Dont_retry(Exception):
    """
    this exception doesn't cause a retry of the edge method when it is raised.
    Useful when a method is not found in the methods object,
    because it would be just a waste of time to retry.
    """

# class Reducer(Thread):
#
#     def __init__(self, state, edges, name=None):
#         super().__init__(name=state['bot'].username)
#         self.name = state['bot'].username
#         self.logger = state['bot'].logger
#         self.edges = edges
#         self.state = state
#
#
#
#     def run(self):
#         get_name = lambda: self.edges[0]['name']
#         name = ignore((KeyError, AttributeError), 'unnamed')(get_name)()
#         self.logger.debug('reducer beginning {} action'.format(name))
#         last_state = reduce(reducer, self.edges, self.state)
#         super().set_data(last_state['data'])
#         return




def reducer(state: dotdict, edge: dotdict):

    bot = state.bot

    if len(state.errors) > 1:
        # tried multiple times
        bot.logger.warning('got lots of errors: {}, bot: {}'.format(state.errors, bot))
        state.errors = []
        # send_bot_to_phone_verifier
        # change_bot_if_neccessary
        # resolve_captcha_if_necessary
        # sleep_more
        # remove_bot_if_broken

    try:

        # if not nodes:
        #     raise Dont_retry('no nodes, {}'.format(nodes))

        method = methods.get(edge.type, None)

        if not method:
            raise Dont_retry('can\'t find method {}'.format(edge.type))

        bot.logger.info(f'# EDGE {edge.type}')


        next_nodes, next_data = method(bot, state.nodes,  edge.args)
        state.data.append(next_data)

        # bot.logger.info('{} did success on {}'.format(type, nodes))
        # bot.logger.debug('{} returned {}'.format(type, next_nodes))

        # next_data = merge(data, {'__{}__'.format(type): next_data})

        # secs = bot.delay[type] if type in bot.delay else bot.delay['usual']
        # time.sleep(secs)

    except (KeyboardInterrupt, SystemExit):
        raise

    except Dont_retry as e:
        bot.logger.error('error reducing edge {}: \"{}\" {}' \
            .format(edge.type, e.__class__.__name__, e))
        return dotdict(nodes=[], bot=bot, errors=state.errors + [e], data=state.data)

    except Exception as exc:
        bot.logger.error('error reducing edge {}: \"{}\" \n {}'.format(
            edge.type,
            exc.__class__.__name__,
            traceback.format_exc()))
        bot.sleep('error')

        # errored_state = dotdict(**merge(state, dotdict(errors=state.errors + [exc])))
        # return reducer(errored_state, edge)
        return dotdict(nodes=[], bot=bot, errors=state.errors + [exc], data=state.data)

    else:
        # all is right, no exceptions
        # bot.logger.warning(state.data)
        # bot.logger.warning(next_data)
        return dotdict(nodes=next_nodes, bot=bot, errors=[], data=state.data)
