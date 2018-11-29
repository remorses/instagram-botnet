from threading import Thread
from types import FunctionType
import datetime


from instabot import API
from .extents import Edges
from .extents import Interactions
from .settings import interaction_delays, total_interactions, max_interactions_per_day


def methods(cls):
    return [x for x, y in cls.__dict__.items() if type(y) == FunctionType]


class BotException(Exception):
    pass


class Bot:

    def __init__(self, username, password, device=None):

        self.start_time = datetime.datetime.now()

        self.api = API(device=device)
        self.api.login(username, password)
        self.logger = self.api.logger
        self.acc = []

        self.total = total_interactions
        self.delays = interaction_delays
        self.max_per_day = max_interactions_per_day

        print('logged as {} {}'.format(username, password))

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

    def reached_limit(self, key):
        current_date = datetime.datetime.now()
        passed_days = (current_date.date() - self.start_time.date()).days
        if passed_days > 0:
            self._reset_counters()
        return self.max_per_day[key] - self.total[key] < 0

    def _reset_counters(self):
        for k in self.total:
            self.total[k] = 0
        self.start_time = datetime.datetime.now()
