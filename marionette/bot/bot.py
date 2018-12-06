import datetime
from pathlib import Path
import json
from ..api import API
from .settings import DELAY, TOTAL, MAX_PER_DAY
from .cache import Cache


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

        self.start_time = datetime.datetime.now()
        self.api = API(log_path=self.log_file, device=device)
        self.logger = self.api.logger

        self.total = TOTAL
        self.delay = DELAY
        self.max_per_day = MAX_PER_DAY

        self.cache_file = make_cache_file(self, cache_path)
        self.log_file = make_log_file(self, log_path)
        self.cookie_file = make_cookie_file(self, cookie_path)


        with open(self.cache_file, 'a+') as file:
            content = file.read()
            content = content if content else '{}'
            data = json.loads(content)
            self.cache = Cache(**data)

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

    def save_cache(self):
        with open(str(self.cache_path / self.username + '_cache.json'), 'w') as file:
            content = json.loads(self.cache)
            file.write(content)

    def _reset_counters(self):
        for k in self.total:
            self.total[k] = 0
        self.start_time = datetime.datetime.now()

def make_cache_file(self, cache_path):

    if not cache_path:
        cache_path = Path(__file__).parents[1] / '_cache'

    cache_path.exists() or cache_path.mkdir()

    return str(cache_path / (self.username + '_cache.json'))

def make_log_file(self, log_path):

    if not log_path:
        log_path = Path(__file__).parents[1] / '_logs'

    log_path.exists() or log_path.mkdir()

    return str(log_path / (self.username + '_logs.html'))

def make_cookie_file(self, cookie_path):

    if not cookie_path:
        cookie_path = Path(__file__).parents[1] / '_cookies'

    cookie_path.exists() or cookie_path.mkdir()

    return str(Path(cookie_path) /'{}_cookie.json'.format(self.username))




class BotException(Exception):
    pass
