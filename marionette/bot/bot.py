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
                 log_path=None,
                 cache_path=None,
                 cookie_path=None,
                 proxy=None,
                 device=None):

        self.id = Bot.id
        self.username = username
        Bot.id += 1

        self.cache_file = make_cache_file(self, cache_path)
        self.log_file = make_log_file(self, log_path)
        self.cookie_file = make_cookie_file(self, cookie_path)

        self.start_time = datetime.datetime.now()
        self.api = API(log_path=self.log_file, id=self.id, device=device)
        self.logger = self.api.logger


        self.total = TOTAL
        self.delay = DELAY
        self.max_per_day = MAX_PER_DAY



        with open(self.cache_file, 'a+') as file:
            content = file.read()
            content = content if content else '{}'
            data = json.loads(content)
            self.cache = Cache(**data)

        self.api.login(username, password, proxy=proxy,
                       cookie_fname=self.cookie_file)



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

    file = Path(str(cache_path.resolve()) + '/' + self.username + '_cache.json')

    file.parent.exists() or file.parent.mkdir()
    file.exists() or file.touch()

    return file.resolve()

def make_log_file(self, log_path):

    if not log_path:
        log_path = Path(__file__).parents[1] / '_logs'

    file = Path(str(log_path.resolve()) + '/' + self.username + '_logs.html')

    file.parent.exists() or file.parent.mkdir()
    file.exists() or file.touch()

    return file.resolve()

def make_cookie_file(self, cookie_path):

    if not cookie_path:
        cookie_path = Path(__file__).parents[1] / '_cookies'

    file = Path(str(cookie_path.resolve()) + '/{}_cookie.json'.format(self.username))

    file.parent.exists() or file.parent.mkdir()
    file.exists() or file.touch()

    return file.resolve()




class BotException(Exception):
    pass
