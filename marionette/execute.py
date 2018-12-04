

from .task import make_task, partitionate
from .reducer import Reducer, make_state, make_actions
from .threads import start, wait


def execute(script, bots):

        data = dict()

        for instruction in script['execute']:
            interaction = list(instruction.keys())[0]

            threads = []
            task = make_task(instruction)

            for (task, bot) in partitionate(task, bots):

                state = make_state(task, bot)
                bot.logger.debug(state)
                actions = make_actions(task)
                bot.logger.debug(actions)
                threads += [Reducer(state, actions)]

            threads = start(threads)
            threads = wait(threads)

            data[interaction] = {'thread' + thread.name: thread.get_data()
                                 for thread in threads}

        return data
