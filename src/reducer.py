from typings import List, Union, TypeVar, Callable
from functoolz import pipe
from edges import Edges
from methods import methods


# def make_edges(edges: str) -> Callable:
#     to_pipe = []
#     for edge in edges.split('->'):
#         to_pipe.append(Edges[edge.strip()])
#     return pipe(*to_pipe)


def identity(method):
    print("can't find the method " + method)
    return method


def reducer(action, argument):
    return methods.get(action.method, identity)(action.arg)


# ogni Edge è una funzione che come input prende sia un Node
# sia una lista di [Node] (se è una lista allora si applica un map
# con la funzione Edge in modo ricorsivo)
