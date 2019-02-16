from .methods import methods
from .nodes import node_classes, Media, User, Arg

class Task(dict):
    """"
    task:

        nodes: [node1, node2] # these are all Node instances

        edges:
            -   type:   feed

            -   type:   send
                args:
                    messages = []
                    stuff =    whokonws

        nodes: [url1, url2]

        edges:
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


def make_task(body):

    nodes = []
    edges = []
    edges = []


    if 'nodes' in body:
        nodes += body['nodes']

    if 'edges' in body:
        for edge in body['edges']:

            if isinstance(edge, dict):
                type = list(edge.keys())[0]
                args = list(edge.values())[0]
                edges += [dict(type=type, args=args)]
            else:
                edges += [dict(type=edge, args={})]
    else:
        raise Exception('in every action there must be actions')

    edges += [dict(type='evaluate', args={})]

    if 'name' in body:
        name = body['name']
        for n, _ in enumerate(edges):
            edges[n]['name'] = name
    else:
        name='not named'

    nodes = initialize_nodes(nodes, edges, body)
    return Task(nodes=nodes, edges=edges, name=name)


# TODO this shit suppress my errors
def partitionate(task: Task, bots):

    couples = []

    for (partition, bot) in enumerate(bots):

        def _right_partition(i):
            return i % len(bots) == partition

        new_nodes = [node for (i, node) in enumerate(task.nodes) if _right_partition(i)]

        new_edges = [dict(**edge) for edge in task.edges]
        new_task = Task(nodes=new_nodes, edges=new_edges)


        couples += [(new_task, bot)]

    return couples


def popped(to_pop, dictionary):
    return {key:value for key, value in dictionary.items() if key != to_pop}



def initialize_nodes(nodes, edges, data):
    if 'from_type' in data:
        Class = node_classes[data['from_type']]
    else:
        first_method = methods.get(edges[0]['type'], None)
        if not first_method:
            raise Exception('can\'t find {} edge in available edges methods')
        Class = first_method.accepts
        Class = Class if Class.__name__ != 'Node' else \
            Media if 'instagram.com' in nodes[0] else Arg

    return [Class(generic=value) for value in nodes]
