from .methods import methods


class Task(dict):
    """"
    task:

        nodes: [node1, node2] # these are all Node instances

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

        edges = [(list(edge.keys())[0], list(edge.values())[0]) for edge in body['via_edges']]
        actions += [dict(type=edge, amount=num, args={}) for (edge, num) in edges]

        actions += [dict(type=interaction, amount=1, args=args)]
    else:
        raise Exception('neither nodes or from_nodes in script')

    print('actions:',actions)

    first_method = methods[actions[0]['type']]
    print('first_method:', first_method.__name__)
    Node = first_method.accepts
    nodes = [Node(generic=node) for node in nodes]

    return Task(nodes=nodes, actions=actions)


def partitionate(task: Task, bots):

    couples = []

    for (partition, bot) in enumerate(bots):

        def _right_partition(i):
            return i % len(bots) == partition

        new_nodes = [node for (i, node) in enumerate(
            task.nodes) if _right_partition(i)]

        new_actions = [dict(**action) for action in task.actions]
        new_task = Task(nodes=new_nodes, actions=new_actions)

        couples += [(new_task, bot)]

    return couples


def popped(to_pop, dictionary):
    return {key:value for key, value in dictionary.items() if key != to_pop}
