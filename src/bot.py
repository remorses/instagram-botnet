from threading import Thread
from functoolz import reduce

from api import API
from reducer import reducer


class Bot(Thread):

    def __init__(self, username, password):
        self.api = API()
        self.api.login(username, password)

    def start(self, script, options):
        reduce(reducer, script['execute'])
        pass
