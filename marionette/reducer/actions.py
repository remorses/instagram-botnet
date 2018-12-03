

class Action(dict):
    pass


def make_actions(task):
        return [_make_action(action) for action in task.actions]


def _make_action(action) -> Action:
        args = action.args if action.args else {}
        return Action(type=action.type, amount=action.amount, args=args)
