from threading import Thread
from instabot import API
from .edges import Edges
from .acts import Acts


class BotException(Exception):
    pass


class Bot:

    def __init__(self, username, password):

        self.api = API(self)
        self.api.login(username, password)
        self.acc = []

        self._edges = Edges(self)
        self._acts = Acts(self)

    def accumulate(self, x):
            self.acc = x

    def do(self, method, arg=[]):
        if method in self._edges:
            t = Thread(target=self._edges[method], args=(self.acc, arg))
            t.start()
            return t
        elif method in self._acts:
            t = Thread(target=self._acts[method], args=(self.acc, arg))
            t.start()
            return t
        else:
            raise BotException("method {} not supported".format(method))
