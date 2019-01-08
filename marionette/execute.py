

from .make_task import make_task, partitionate
from .make_bots import make_bots
from .reducer import Reducer, State, Action
from .threads import start, wait


def execute(script,):

    bots = make_bots(script)

    script_name = script['name'] if script['name'] else 'unnmaed script'

    data = dict()

    try:
        for instruction in script['execute']:
            interaction = list(instruction.keys())[0]

            threads = []
            task = make_task(instruction)

            for (task, bot) in partitionate(task, bots):
                bot.logger.debug('nodes in execute: %s' % task.nodes)
                state = dict(nodes=task.nodes, bot=bot, data=dict(), errors=[])
                # bot.logger.debug(str(bot) + ' ' + str(state))
                actions = [Action(type=action['type'], args=action['args']) for action in task.actions]
                # bot.logger.debug(actions)
                threads += [Reducer(state, actions)]
                bot.logger.debug('new task of type {} and new thread, in script {}'.format(interaction, script_name))
                bot.logger.debug('actions : {}, nodes: {}'.format(actions, list(state['nodes'])))


            threads = start(threads)
            threads = wait(threads)

            data['__' + interaction + '_interaction__'] = [thread.get_data() for thread in threads]
            # {'thread' + thread.name: thread.get_data() for thread in threads}


    except KeyboardInterrupt:
        bot.logger.warn('keyboard interrupt')
        raise


    finally:
        return data
