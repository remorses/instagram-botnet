import datetime
from pathlib import Path

from ..api import API
from .settings import DELAY, TOTAL, MAX_PER_DAY


class Bot:

    id = 0

    def __init__(
                 self,
                 username,
                 password,
                 log_path='',
                 cookie_path='',
                 proxy=None,
                 device=None):

        self.id = Bot.id
        self.username = username
        Bot.id += 1

        if not cookie_path:
            cookie_file = '{}_cookie.json'.format(username)
            cookie_path = str(
                Path(__file__).parents[1] / '_cache' / cookie_file)

        if not log_path:
            log_file = '{}_logs.html'.format(username)
            log_path = str(Path(__file__).parents[1] / '_logs' / log_file)

        self.start_time = datetime.datetime.now()

        self.api = API(log_path=log_path, device=device)
        self.logger = self.api.logger

        self.total = TOTAL
        self.delay = DELAY
        self.max_per_day = MAX_PER_DAY

        self.api.login(username, password, proxy=proxy,
                       cookie_fname=cookie_path)

    def __repr__(self):
        return 'Bot(username=\'{}\', id={})'.format(self.username, self.id)

    @property
    def last(self):
        return self.api.last_json

    def reached_limit(self, key):
        current_date = datetime.datetime.now()
        passed_days = (current_date.date() - self.start_time.date()).days
        if passed_days > 0:
            self._reset_counters()
        return self.max_per_day[key] - self.total[key] < 0

    def filter(self, nodes):
        """
        this method will be overwritten in the prepare phase
        """
        return nodes

    def _reset_counters(self):
        for k in self.total:
            self.total[k] = 0
        self.start_time = datetime.datetime.now()


class BotException(Exception):
    pass
