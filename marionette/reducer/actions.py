

class Action(dict):
    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            raise AttributeError("No such attribute: " + name)

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        if name in self:
            del self[name]
        else:
            raise AttributeError("No such attribute: " + name)


def make_actions(task):
        return [_make_action(action) for action in task.actions]


def _make_action(action) -> Action:
        args = action.args if action.args else {}
        return Action(type=action.type, amount=action.amount, args=args)
