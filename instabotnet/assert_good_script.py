from .methods import methods
from .nodes import node_classes



class MalformedScript(Exception):
    pass


def assert_good_script(script):
    for action in script['actions']:
    
        if not 'name' in action:
            raise MalformedScript('missing `name` in some action')
            
        name = action['name']
        
        if not 'from' in action:
            raise MalformedScript(f'missing `from` in action {name}')
        
        if not 'edges' in action:
            raise MalformedScript(f' missing `edges` in action {name}')
        
        if not 'nodes' in action:
            raise MalformedScript(f' missing `nodes` in action {name}')
        
        for edge in [edge.keys()[0] if isinstance(edge, dict) else edge for edge in action['edges']]:
            if not edge in methods:
                raise MalformedScript(f'unknown edge {edge} in action {name}')
            
        check, problem = check_edges(action['edges'], action['from'])
        
        if not check:
            raise MalformedScript(f'wrong edges chaining in action {name}, {problem}')


def check_edges(from_type, edges):
    reducer = lambda acc, name: methods[name].accepts \
        if isinstance(acc, methods[name].accepts,) and acc is not None \
        else None
        
    reducer = lambda edges, last: edges + [last] \
        if methods[edges[-1]] is not None \
        and  isinstance(methods[edges[-1]]['returns'], methods[last]['accepts']) \
        else edges + [None]
        
    names = [edge.keys()[0] if isinstance(edge, dict) else edge for edge in edges]
    
    
    checks = reduce(reducer, names, [dict(returns=node_classes[from_type])])
    
    if None in checks:
        index = checks.index(None)
        errored_edge = names[index]
        right_type = methods[errored_edge].accepts
        wrong_type = methods[names[index - 1]].accepts if index > 0 else from_type
        problem = f'{errored_edge} must receive nodes of type {right_type}, not {wrong_type}'
        return False, problem
        
    else:
        return True, ''


