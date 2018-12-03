

from .prepare import make_bots
from .task import make_task, partitionate, Task
from .reducer import Reducer, make_state, make_actions
from .threads import start, wait, reset

script = {}

bots = make_bots(script)

for data in script['execute']:

    threads = reset()
    task: Task = make_task(data)

    for (task, bot) in partitionate(task, bots):
        state = make_state(task, bot)
        actions = make_actions(task)
        threads += [Reducer(state, actions)]

    threads = start(threads)
    threads = wait(threads)
    threads = reset(threads)
