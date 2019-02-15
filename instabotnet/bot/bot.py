import datetime
from pathlib import Path
import dataset
import json
import time
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
                 logs_file=None,
                 cache_file=None,
                 cookie_file=None,
                 proxy=None,
                 device=None):

        self.cache_file = make_cache_file(cache_file, username + '_cache.db')
        self.logs_file = make_logs_file( logs_file, username + '_logs.html')
        self.cookie_file = make_cookie_file(cookie_file, username + '_cookie.json')

        self.id = Bot.id
        self.username = username
        Bot.id += 1

        self.predicates = [] # [partial(not_in_cache, self), ]

        self.start_time = datetime.datetime.now()
        self.api = API(logs_file=self.logs_file, id=self.id, username=username, device=device)
        self.logger = self.api.logger

        self.total = TOTAL
        self.delay = DELAY
        self.max_per_day = MAX_PER_DAY

        # methods used in propertis used in yaml
        self._followers_ids = []
        self._followers_usernames = []
        self._following_ids = []
        self._following_usernames = []



        self.api.login(username, password, proxy=proxy, use_cookie=True,
                       cookie_fname=self.cookie_file)



    def __repr__(self):
        return 'Bot(username=\'{}\', id={})'.format(self.username, self.id)

    @property
    def cache(self):
        return dataset.connect(make_db_url(self.cache_file), engine_kwargs = {'connect_args': {'check_same_thread' : False}})

    @property
    def followers_ids(self):
            if self._followers_ids:
                print(self._followers_ids)

                return self._followers_ids
            else:
                data = cycled_api_call(99999, self, self.api.get_user_followers, id, 'users')
                user_ids = map(lambda item: item['pk'], data)
                self._followers_ids = list(user_ids)
                print(self._followers_ids)
                return self._followers_ids


    @property
    def last(self):
        if self.api.last_json:
            return self.api.last_json
        else:
            return {}

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

        return nodes

    def suitable(self, node, **kwargs):
        """
        same as filter but only one node, returns True if node in suitable
        """
        bool = True

        for predicate in self.predicates:
            bool = bool and predicate(
                node,
                **kwargs
            )

        return bool


    def sleep(self, type='usual'):

        if type in self.delay:
            self.logger.debug('sleeping for {} seconds'.format(self.delay[type]))
            time.sleep(self.delay[type])
        else:
            self.logger.debug('sleeping for {} seconds'.format(self.delay['usual']))
            time.sleep(self.delay['usual'])


    def _reset_counters(self):
        for k in self.total:
            self.total[k] = 0
        self.start_time = datetime.datetime.now()




def make_db_url( file):
    return 'sqlite:///{}'.format(str(file.resolve()))

def make_logs_file( file, name):
    if not file:
        file = Path(str(Path('.') / '_logs' / name)).resolve()
        file.parent.exists() or file.parent.mkdir()
    file = Path(file)
    file.exists() or file.touch()
    return str(file.resolve())

def make_cache_file( file, name):
    if not file:
        file = Path(str(Path('.') / '_cache' / name)).resolve()
        file.parent.exists() or file.parent.mkdir()
    file = Path(file)
    file.exists() or file.touch()
    return file.resolve()

def make_cookie_file( file, name):
    if not file:
        file = Path(str(Path('.') / '_cookies' / name)).resolve()
        file.parent.exists() or file.parent.mkdir()
    file = Path(file)
    file.exists() or file.touch()
    return str(file.resolve())


def cycled_api_call(amount, bot, api_method, api_argument, key,  ):

    next_max_id = ''
    sleep_track = 0
    done = 0


    while True:
        bot.logger.info('new get cycle with %s' % api_method.__name__)
        try:
            api_method(api_argument, max_id=next_max_id)
            items = bot.last[key] if key in bot.last else []

            if 'next_max_id' not in bot.last:
                yield from items
                done += len(items)
                return

            elif "more_available" in bot.last and not bot.last["more_available"]:
                yield from items
                done += len(items)
                return

            elif "big_list" in bot.last and not bot.last['big_list']:
                yield from items
                done += len(items)
                return

            # elif (done + len(items)) >= max:
            #     yield from items[:(max - done)]
            #     done += len(items)
            #     return

            else:
                yield from items
                done += len(items)

        except Exception as exc:
            bot.logger.error('exception in cycled_api_call: {}'.format(exc))
            yield from []
            return

        if sleep_track > 10:
            bot.logger.debug('sleeping some time while getting')
            bot.sleep('getter')
            sleep_track = 0

        bot.sleep('usual')
        next_max_id = bot.last.get("next_max_id", "")
        sleep_track += 1
