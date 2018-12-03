class State(dict):
    pass


def make_state(task, bot):
        state = State(target_nodes=task.nodes, bot=bot, errors=[])
        return state
