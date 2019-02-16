from .methods import methods
from .nodes import node_classes, Media, User, Arg
from .support import dotdict
from functools import reduce



def nodes_edges(body):

    nodes = []
    edges = []

    if 'nodes' in body:
        nodes += body['nodes']

    if 'edges' in body:
        for edge in body['edges']:

            if isinstance(edge, dict):
                type = list(edge.keys())[0]
                args = list(edge.values())[0]
                edges += [dotdict(type=type, args=args)]
            else:
                edges += [dotdict(type=edge, args={})]
    else:
        raise Exception('in every action there must be edges')

    info = dotdict(
        name=body['name'] if 'name' in body else 'not named',
        total_nodes=reduce(lambda acc, e: e.args.get('amount', 1) * acc, edges, 1),
    )

    edges += [dotdict(type='evaluate', args=dict(info=info))]

    nodes = initialize_nodes(nodes, edges, body)

    return nodes, edges






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
