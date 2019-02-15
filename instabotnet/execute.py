

from .make_task import make_task, partitionate
from .make_bots import make_bots
from .populate import populate_object, populate_string
from .reducer import Reducer
from .threads import start, wait
import yaml
import traceback

def execute(script, variables={}):

    if isinstance(script, str):
        script = populate_string(script, variables)
        if '{{' in script:
            var = locate_variable(script)
            raise Exception('yaml file needs all data to be populated: {{{{ {} }}}}'.format(var))
        script = yaml.load(script)
    else:
        script = populate_object(script, variables)

    bots = make_bots(script)

    script_name = script['name'] if 'name' in script else 'unnmaed script'

    data = dict()

    try:
        for instruction in script['actions']:
            interaction = list(instruction.keys())[0]

            threads = []
            task = make_task(instruction)

            for (task, bot) in partitionate(task, bots):
                # bot.logger.debug('nodes in execute: %s' % task.nodes)
                state = dict(nodes=task.nodes, bot=bot, data=dict(), errors=[])
                # bot.logger.debug(str(bot) + ' ' + str(state))
                edges = [dict(type=edge['type'], args=edge['args']) for edge in task.edges]
                # bot.logger.debug(edges)
                threads += [Reducer(state, edges)]
                bot.logger.debug('edges : {}, nodes: {}'.format(edges, list(state['nodes'])))


            threads = start(threads)
            threads = wait(threads)

            data['__' + interaction + '_interaction__'] = [thread.get_data() for thread in threads]
            # {'thread' + thread.name: thread.get_data() for thread in threads}


    except KeyboardInterrupt:
        bot.logger.warn('keyboard interrupt')
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

    finally:
        return data

def locate_variable(script):
    begin = script.index('{{')
    end = script.index('}}', begin )
    return script[begin:end].replace('{{', '').strip()
