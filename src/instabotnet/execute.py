from .nodes_edges import nodes_edges
from .make_bot import make_bot
from .populate import populate_object, populate_string
from .assert_good_script import assert_good_script
from .reducer import  reducer
from .support import dotdict, merge
from collections import deque
from functools import reduce
import time
import traceback
import os
import re
import yaml
from .notification_events import notification_events
from .api.instagram_private_api.errors import (
    ClientError,
    ClientLoginRequiredError,
    ClientCookieExpiredError,
    ClientConnectionError,
    ClientThrottledError,
    ClientLoginError,
    ClientReqHeadersTooLargeError,
    ClientCheckpointRequiredError,
    ClientChallengeRequiredError,
    ClientSentryBlockError,
)

yaml.reader.Reader.NON_PRINTABLE = re.compile(
    u'[^\x09\x0A\x0D\x20-\x7E\x85\xA0-\uD7FF\uE000-\uFFFD\U00010000-\U0010FFFF]')


DEBUG = bool(os.environ.get('DEBUG'))

def execute(script_string, variables={}) -> [dict]:

    if "---" in script_string:
        scripts = script_string.split('---')
        def _reducer(acc, script):
            nonlocal variables
            variables.update(acc)
            return merge(acc, execute(script, variables))
        return reduce(_reducer, scripts, {})

    
    script = obj_from_yaml(script_string, variables)

    assert_good_script(script)

    try:
        bot = make_bot(script, variables)
        
    except ClientCheckpointRequiredError as e:
        print(str(e))
        raise e from None
        
    except ClientSentryBlockError as e:
        print(str(e))
        raise e from None

    except ClientError as e:
        print(str(e))
        raise e from None



    script_name = script['name'] if 'name' in script else 'unnmaed script'
    bot.logger.info(f'# SCRIPT {script_name}')

    result = deque()

    try:
        for action in script['actions']:
            action_name = action['name'] if 'name' in action else 'unnmaed action'
            bot.logger.info(f'# ACTION {action_name}')

            nodes, edges = nodes_edges(action, bot)
            start_data = { 'events': notification_events(bot) }

            begin_state = dotdict(nodes=(node for node in nodes), bot=bot, data=deque([start_data]), errors=[])
            bot.logger.info(f'# with nodes {nodes}')

            end_state = reduce(reducer, edges, begin_state)
            result.extend(end_state['data'])

    except (KeyboardInterrupt, SystemExit):
        bot.logger.warning('keyboard interrupt')
        raise

    except Exception as exc:
        print(
            exc.__class__.__name__,
            ':',
            exc,
            '\n',
            '\n'.join(traceback.format_exc().split('\n'))
        )
        raise

    else:
        result = dict(reduce(merge, result))
        return result



def obj_from_yaml(script, variables):
    if isinstance(script, str):
        script = populate_string(script, variables)
        return yaml.safe_load(script)
    else:
        return populate_object(script, variables)





    # try:
    #     for action in script['actions']:
    #
    #
    #
    #         threads = []
    #         task = make_task(action)
    #         name = task['name']
    #
    #         for (task, bot) in partitionate(task, bots):
    #             state = dict(nodes=task.nodes, bot=bot, data=dict(), errors=[])
    #             threads += [Reducer(state, task.edges)]
    #             # bot.logger.debug('edges : {}, nodes: {}'.format(edges, list(state['nodes'])))
    #
    #
    #         threads = start(threads)
    #         threads = wait(threads)
    #
    #         data['__' + interaction + '_interaction__'] = [thread.get_data() for thread in threads]
    #         # {'thread' + thread.name: thread.get_data() for thread in threads}
