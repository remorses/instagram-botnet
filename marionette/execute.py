

from .task import make_task, partitionate
from .reducer import Reducer, make_state, make_actions
from .threads import start, wait


def execute(bots, script):

    for data in script['execute']:

        threads = []
        task = make_task(data)

        for (task, bot) in partitionate(task, bots):
            state = make_state(task, bot)
            actions = make_actions(task)
            threads += [Reducer(state, actions)]

        threads = start(threads)
        threads = wait(threads)
