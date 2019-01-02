import datetime
from pathlib import Path
import dataset
import json
from funcy import partial
from ..api import API
from .settings import DELAY, TOTAL, MAX_PER_DAY
from .predicates import not_in_cache

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
        self.cache_path = cache_path
        Bot.id += 1

        self.log_file = make_log_file( log_path, username + '_logs.html')
        self.cookie_file = make_cookie_file(cookie_path, username + '_cookie.json')


        self.predicates = [partial(not_in_cache, self), ]

        self.start_time = datetime.datetime.now()
        self.api = API(log_path=self.log_file, id=self.id, username=username, device=device)
        self.logger = self.api.logger

        self.total = TOTAL
        self.delay = DELAY
        self.max_per_day = MAX_PER_DAY


        self.api.login(username, password, proxy=proxy,
                       cookie_fname=self.cookie_file)



    def __repr__(self):
        return 'Bot(username=\'{}\', id={})'.format(self.username, self.id)

    @property
    def cache(self):
        return dataset.connect(make_db_url(self.cache_path, self.username + '_cache.db'))



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
        this filters every node before an interaction,
        you can customize this bychanging the predicates.
        prediacte is a function that takes a node as argument
        and returns a boolean
        """
        for predicate in self.predicates:
            nodes = filter(predicate, nodes)

    def suitable(self, node):
        """
        same as filter but only one node, returns True if node in suitable
        """
        bool = True

        for predicate in self.predicates:
            bool = bool and predicate(node)

        return bool


    def _reset_counters(self):
        for k in self.total:
            self.total[k] = 0
        self.start_time = datetime.datetime.now()




def make_db_url(cache_path, name):
    if not cache_path:
        cache_path = Path('.') / '_cache'

    cache_path.exists() or cache_path.mkdir()
    path = str(cache_path.resolve() / name)

    return 'sqlite:///{}'.format(path)

def make_log_file( log_path, name):

    if not log_path:
        log_path = Path('.') / '_logs'

    file = Path(str(log_path.resolve()) + '/' + name)

    file.parent.exists() or file.parent.mkdir()
    file.exists() or file.touch()

    return file.resolve()

def make_cookie_file( cookie_path, name):

    if not cookie_path:
        cookie_path = Path('.') / '_cookies'

    file = Path(str(cookie_path.resolve() / name))

    file.parent.exists() or file.parent.mkdir()
    file.exists() or file.touch()

    return file.resolve()
