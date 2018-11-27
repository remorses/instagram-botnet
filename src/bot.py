from threading import Thread
from functoolz import reduce

from instabot import API
from reducer import reducer
from .edges import Edges
from .acts import Acts


class Bot(Thread):

    def __init__(self, username, password):
        self.api = API(self)
        self.api.login(username, password)
        self.edges = Edges(self)
        self.acts = Acts(self)
        self.acc = []

    def start(self, method, arg):
        if method in self.edges:
            next_arg = self.edges[method](arg)
            self.acc.append(next_arg)
        elif method in self.acts:
            self.acts[method](arg)
        else:
            raise Exception("methd {} not supported".format(method))
