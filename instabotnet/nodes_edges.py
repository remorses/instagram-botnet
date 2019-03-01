from .methods import methods
from .nodes import Arg, Media, node_classes
from .support import dotdict
from funcy import rcompose
from instagram_private_api.utils import InstagramID
from instagram_private_api import Client
from functools import reduce



def nodes_edges(body, bot):

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

    nodes = initialize_nodes(nodes, body['from'], bot)

    return nodes, edges



def calc_total_nodes(acc, edge):
    amount  = edge.args.get('amount', 1)
    max = edge.args.get('max', acc)
    return amount * acc if acc <= max else max


def initialize_nodes(nodes, from_type, bot):

    api: Client = bot.api

    Class = node_classes[from_type.lower()]

    switch = {
        'User': lambda username: api.username_info(username)['user'],
        'Media': rcompose(
            lambda url: [x for x in url.split('/') if x][-1],
            lambda short: InstagramID.expand_code(short),
            lambda code: api.media_info(code),
        ),
        'Hashtag': lambda name: {'name': name},
        'Arg': lambda x: x,
        'Geotag': lambda name: api.location_search(bot.latitude, bot.longitude, query=name, )
    }


    return [Class(data=switch[Class.__name__](value)) for value in nodes]
