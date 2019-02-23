from .methods import methods
from .nodes import Arg, Media, node_classes
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
                args = args if isinstance(args, dict) else {}
                edges += [dotdict(type=type, args=args)]
            else:
                edges += [dotdict(type=edge, args={})]
    else:
        raise Exception('in every action there must be edges')

    info = dotdict(
        name=body['name'] if 'name' in body else 'not named',
        total_nodes=reduce(calc_total_nodes, edges, len(nodes)),
    )

    edges += [dotdict(type='evaluate', args=dict(info=info))]

    nodes = initialize_nodes(nodes, edges, body)

    return nodes, edges



def calc_total_nodes(acc, edge):
    amount  = edge.args.get('amount', 1)
    max = edge.args.get('max', acc)
    return amount * acc if acc <= max else max


def initialize_nodes(nodes, edges, data):
    if 'from_type' in data:
        Class = node_classes[data['from_type'].lower()]
    elif 'from' in data:
        Class = node_classes[data['from'].lower()]
    else:
        first_method = methods.get(edges[0]['type'], None)
        if not first_method:
            raise Exception('can\'t find {} edge in available edges methods')
        Class = first_method.accepts
        Class = Class if Class.__name__ != 'Node' else \
            Media if 'instagram.com' in nodes[0] else Arg

    return [Class(generic=value) for value in nodes]


