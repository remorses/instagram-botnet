

from .task import make_task, partitionate
from .reducer import Reducer, make_state, make_actions
from .threads import start, wait


def execute(script, bots):

    script_name = script['name'] if script['name'] else 'unnmaed script'

    data = dict()

    try:
        for instruction in script['execute']:
            interaction = list(instruction.keys())[0]

            threads = []
            task = make_task(instruction)

            for (task, bot) in partitionate(task, bots):
                state = make_state(task, bot)
                # bot.logger.debug(str(bot) + ' ' + str(state))
                actions = make_actions(task)
                # bot.logger.debug(actions)
                threads += [Reducer(state, actions)]
                bot.logger.debug('new task of type {} and new thread, in script {}'.format(interaction, script_name))


            threads = start(threads)
            threads = wait(threads)

            data['__' + interaction + '_interaction__'] = [thread.get_data() for thread in threads]
            # {'thread' + thread.name: thread.get_data() for thread in threads}


    except KeyboardInterrupt:
        raise

    except Exception as e:
        raise e

    finally:
        return data
