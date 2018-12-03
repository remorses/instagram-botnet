
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
    pass


def make_task(data):

    nodes = []
    actions = []
    args = {}

    interaction, body = data.items()[0]

    if 'nodes' in body:
        nodes += body['nodes']
        args = body['args']
        actions += [dict(type=interaction, amount=1)]

    elif 'from_nodes' in body:
        nodes += body['from_nodes']
        args = body['args']
        edges = body['via_edges']
        actions += [dict(type=edge, amount=num, args=[])
                    for (edge, num) in edges]
        actions += [dict(type=interaction, amount=1, args=args)]
    else:
        raise Exception

    return Task(nodes=nodes, actions=actions)


def partitionate(task: Task, bots):

    couples = []

    for (partition, bot) in enumerate(bots):

        def _right_partition(i): return i % len(bots) == partition
        new_nodes = [node for (i, node) in enumerate(
            task.nodes) if _right_partition(i)]
        new_task = Task(nodes=new_nodes, amount=task.amount, args=task.args)
        couples += [(new_task, bot)]

    return couples
