from threading import Thread
from functoolz import reduce

from api import API
from reducer import reducer
from .edges import Edges
from .acts import Acts


class Bot(Thread):

    def __init__(self, username, password):
        self.api = API(self)
        self.api.login(username, password)
        self.edges = Edges()
        self.acts = Acts()
        self.accumulator = []

    def start(self, method, arg):
        if method in self.edges:
            next_arg = self.edges[edge](arg)
            self.accumulator.append(next_arg)
        elif method in self.acts:
            self.acts[act](arg)

    def like(self, users):
