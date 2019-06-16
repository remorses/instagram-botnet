from .methods import methods
from .nodes import Arg, Media, node_classes
from .support import dotdict
from funcy import rcompose
from .api.instagram_private_api.utils import InstagramID
from .api.instagram_private_api import Client
from functools import reduce
from .handle_errors import handle


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
                # args = args if isinstance(args, dict) else {} # support sleep: Int
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
    amount  = int(edge.args.get('amount', 1)) if isinstance(edge.args, dict) else 1
    max = edge.args.get('max', acc) if isinstance(edge.rgs, dict) else acc
    return amount * acc if acc <= max else max


def initialize_nodes(nodes, from_type, bot):

    api: Client = bot.api

    Class = node_classes[from_type.lower()]

    switch = {
        'User': lambda username: api.username_info(username)['user'],
        'Media': rcompose(
            lambda url: [x for x in url.split('/') if x][-1],
            lambda short: InstagramID.expand_code(short),
            lambda id: api.media_info(id),
            lambda data: data['items'][0],
            # lambda x: print(x) or x
        ),
        'Hashtag': lambda name: {'name': name},
        'Arg': lambda v: {'value': v},
        'Geotag': lambda name: api.location_search(bot.latitude, bot.longitude, query=name,)['venues'][0]
    }

    try:
        return handle(lambda: [Class(**switch[Class.__name__](value)) for value in nodes], bot)

    except Exception as e:
        bot.logger.error(f'error initializing nodes {nodes}: {e}')
        raise e from None
        return []
