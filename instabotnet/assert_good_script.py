from .methods import methods
from .nodes import node_classes


def assert_good_script(script):
    for action in script['actions']:
        if not 'from' in action:
            raise
        
        if not 'edges' in action:
            raise
        
        if not 'nodes' in action:
            raise
        
        if not check_edges(action['edges'], action['from']):
            raise


def check_edges(from, edges):
    reducer = lambda acc, name: isinstance(methods[name].accepts, acc)
    names = [edge.keys()[0] for edge in edges]
    checks = reduce(reducer, names, node_classes[from])
    return all(checks)