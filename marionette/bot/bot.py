from threading import Thread
from types import FunctionType
from instabot import API
from .extents import Edges
from .extents import Interactions


def methods(cls):
    return [x for x, y in cls.__dict__.items() if type(y) == FunctionType]


class BotException(Exception):
    pass


class Bot:

    def __init__(self, username, password, device=None):

        self.api = API(device=device)
        self.api.login(username, password)
        print('logged as {} {}'.format(username, password))
        self.acc = []

        self._edges = Edges(self)
        self._interactions = Interactions(self)

    def accumulate(self, x):
            self.acc.append(x)

    def reset(self):
            self.acc = []

    def do(self, method, arg=[]):
        print('doing {}'.format(method))
        if method in methods(Edges):
            print('doing a edge scrape {} with arg {} and acc {}'.format(
                method, arg, self.acc))
            t = Thread(target=self._edges[method], args=(arg,))
            t.start()
            return t
        elif method in methods(Interactions):
            print('doing an interaction {} with arg {} and acc {}'.format(
                method, arg, self.acc))
            t = Thread(target=self._interactions[method], args=(arg,))
            t.start()
            return t
        else:
            raise BotException("method {} not supported".format(method))
