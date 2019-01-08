from .methods import methods
from .nodes import  Media, User

class Task(dict):
    """"
    task:

        nodes: [node1, node2] # these are all Node instances

        actions:
            -   type:   feed

            -   type:   send
                args:
                    messages = []
                    stuff =    whokonws

        nodes: [url1, url2]

        actions:
            -   type: upload
                args:
                    caption: 'text bla bla'
                    location: id
                    usertags: id

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
        edges = body['edges']
        args = body['args'] if 'args' in body else {}
        args['amount'] = body['amount'] if 'amount' in body \
            else args['amount'] if 'amount' in args \
            else 1
        actions += [dict(type=edge, args={}) for edge in edges]
        actions += [dict(type=interaction, args=args)]

    else:
        raise Exception('nodes not in script in script')
        
    nodes = initialize_nodes(nodes, actions)
    return Task(nodes=nodes, actions=actions)


def partitionate(task: Task, bots):

    couples = []

    for (partition, bot) in enumerate(bots):

        def _right_partition(i):
            return i % len(bots) == partition

        new_nodes = [node for (i, node) in enumerate(task.nodes) if _right_partition(i)]

        new_actions = [dict(**action) for action in task.actions]
        new_task = Task(nodes=new_nodes, actions=new_actions)


        couples += [(new_task, bot)]

    return couples


def popped(to_pop, dictionary):
    return {key:value for key, value in dictionary.items() if key != to_pop}



def initialize_nodes(nodes, actions, ):
    first_method = methods.get(actions[0]['type'], None)
    if not first_method:
        raise Exception('can\'t find {} interaction in available methods')
    Class = first_method.accepts
    Class = Class if Class.__name__ != 'Node' else \
        Media if 'instagram.com' in nodes[0] else User

    return [Class(generic=value) for value in nodes]
