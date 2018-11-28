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

        self.edges = Edges(self)
        self.acts = Acts(self)

    def do(self, method, arg=[]):
        if method in self.edges:
            t = Thread(target=self.edges[method], args=(self.acc, arg))
            t.start()
            return t
        elif method in self.acts:
            t = Thread(target=self.acts[method], args=(self.acc, arg))
            t.start()
            return t
        else:
            raise BotException("method {} not supported".format(method))
