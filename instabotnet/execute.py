

# from .make_task import make_task, partitionate
from .nodes_edges import nodes_edges
from .make_bots import make_bots
from .populate import populate_object, populate_string
from .reducer import  reducer
from .support import dotdict
from collections import deque
from functools import reduce
# from .threads import start, wait
import traceback

from ruamel.yaml import YAML

yaml = YAML()

def execute(script, variables={}) -> [dict]:

    script = obj_from_yaml(script, variables)

    bot = make_bots(script)[0]

    script_name = script['name'] if 'name' in script else 'unnmaed script'
    bot.logger.info(f'# SCRIPT {script_name}')

    result = deque()

    try:
        for action in script['actions']:
            action_name = action['name'] if 'name' in action else 'unnmaed action'
            bot.logger.info(f'# ACTION {action_name}')

            nodes, edges = nodes_edges(action)
            begin_state = dotdict(nodes=nodes, bot=bot, data=deque([]), errors=[])
            bot.logger.info(f'# with nodes {nodes}')

            end_state = reduce(reducer, edges, begin_state)
            result.extend(end_state['data'])

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


    except KeyboardInterrupt:
        bot.logger.warn('keyboard interrupt')
        exit(0)

    except Exception as exc:
        print(
            exc.__class__.__name__,
            ':',
            exc,
            '\n',
            '\n'.join(traceback.format_exc().split('\n'))
        )
        raise

    finally:
        return result

def locate_variable(script):
    begin = script.index('{{')
    end = script.index('}}', begin )
    return script[begin:end].replace('{{', '').strip()


def obj_from_yaml(script, variables):
    if isinstance(script, str):
        script = populate_string(script, variables)
        if '{{' in script:
            var = locate_variable(script)
            raise Exception('yaml file needs all data to be populated: {{{{ {} }}}}'.format(var))
        return yaml.load(script)
    else:
        return populate_object(script, variables)
