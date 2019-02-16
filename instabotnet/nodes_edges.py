from .methods import methods
from .nodes import node_classes, Media, User, Arg




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
                edges += [dict(type=type, args=args)]
            else:
                edges += [dict(type=edge, args={})]
    else:
        raise Exception('in every action there must be edges')

    edges += [dict(type='evaluate', args={})]

    if 'name' in body:
        name = body['name']

    else:
        name='not named'

    for n, _ in enumerate(edges):
        edges[n]['name'] = name

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
