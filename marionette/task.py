
class Task(dict):
    """"
    task:

        nodes: [node1, node2]



        actions:

                - type:   feed
                  amount: 10

                - type:   send
                  amount: 1
                  args:
                    messages = []
                    stuff =    whokonws
    """

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


def make_task(data):

    nodes = []
    actions = []
    args = {}

    interaction, body = list(data.items())[0]

    if 'nodes' in body:
        nodes += body['nodes']
        args = body['args'] if 'args' in body else {}
        actions += [dict(type=interaction, amount=1)]

    elif 'from_nodes' in body:
        nodes += body['from_nodes']
        args = body['args'] if 'args' in body else {}
        edges = body['via_edges']
        actions += [dict(type=edge, amount=num, args={})
                    for (edge, num) in edges]
        actions += [dict(type=interaction, amount=1, args=args)]
    else:
        raise Exception

    return Task(nodes=nodes, actions=actions)


def partitionate(task: Task, bots):

    couples = []

    for (partition, bot) in enumerate(bots):

        def _right_partition(i):
            return i % len(bots) == partition

        new_nodes = [node for (i, node) in enumerate(
            task.nodes) if _right_partition(i)]

        new_actions = [dict(args=[], **action) for action in task.actions]
        new_task = Task(nodes=new_nodes, actions=new_actions)

        couples += [(new_task, bot)]

    return couples
