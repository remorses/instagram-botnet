import datetime
from pathlib import Path

from ..api import API
from .settings import interaction_delays, total_interactions, max_interactions_per_day


class Bot:

    def __init__(
                 self,
                 username,
                 password,
                 log_path='',
                 cookie_path='',
                 proxy=None,
                 device=None):

        if not cookie_path:
            cookie_file = '{}_cookie.json'.format(username)
            cookie_path = str(
                Path(__file__).parents[1] / 'cache' / cookie_file)

        if not log_path:
            log_file = '{}_logs.html'.format(username)
            log_path = str(Path(__file__).parents[1] / 'logs' / log_file)

        self.start_time = datetime.datetime.now()

        self.api = API(log_path=log_path, device=device)
        self.logger = self.api.logger

        self.total = total_interactions
        self.delay = interaction_delays
        self.max_per_day = max_interactions_per_day

        self.api.login(username, password, proxy=proxy,
                       cookie_fname=cookie_path)

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


class BotException(Exception):
    pass
