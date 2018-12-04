import datetime
from pathlib import Path
import json
from ..api import API
from .settings import DELAY, TOTAL, MAX_PER_DAY


class Bot:

    id = 0

    def __init__(
                 self,
                 username,
                 password,
                 log_path='',
                 cache_path='',
                 cookie_path='',
                 proxy=None,
                 device=None):

        self.id = Bot.id
        self.username = username
        Bot.id += 1

        self.cache_path = cache_path

        if not cache_path:
            self.cache_path = Path(__file__).parents[1] / '_cache'
            if not self.cache_path.exists():
                self.cache_path.mkdir()

        if not cookie_path:
            cookie_file = '{}_cookie.json'.format(username)
            cookie_path = str(self.cache_path / cookie_file)

        if not log_path:
            log_path = Path(__file__).parents[1] / '_logs'
            if not log_path.exists():
                log_path.mkdir()

        self.start_time = datetime.datetime.now()

        log_file = str(log_path / (username + '_logs.html'))

        self.api = API(log_path=log_file, device=device)
        self.logger = self.api.logger

        self.total = TOTAL
        self.delay = DELAY
        self.max_per_day = MAX_PER_DAY

        self.api.login(username, password, proxy=proxy,
                       cookie_fname=cookie_path)

        with open(str(self.cache_path / (username + '_cache.json')), 'a+') as file:
            content = file.read()
            content = content if content else '{}'
            cache = json.loads(content)

        self.cache = cache

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

    def save_cache(self):
        with open(str(self.cache_path / self.username + '_cache.json'), 'w+') as file:
            content = json.loads(self.cache)
            file.write(content)

    def _reset_counters(self):
        for k in self.total:
            self.total[k] = 0
        self.start_time = datetime.datetime.now()



class BotException(Exception):
    pass
