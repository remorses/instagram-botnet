import datetime
from pathlib import Path
import time
from ..api import API
from instagram_private_api import  ClientCookieExpiredError, ClientLoginRequiredError
from .support import to_json, from_json
from .settings import DELAY, TOTAL, MAX_PER_DAY
import json









class Bot:

    id = 0

    def __init__(
                 self,
                 username,
                 password,
                 # cookie_file=None,
                 settings_file=None,
                 proxy=None,
                 device=None):

        # self.cookie_file = make_cookie_file(cookie_file, username + '_cookie.json')
        self.settings_file = make_file(settings_file, username + '_settings.json', initial='{}')

        self.id = Bot.id
        self.username = username
        self.password = password
        self.proxy = proxy
        Bot.id += 1

        self.predicates = [] # [partial(not_in_cache, self), ]

        self.start_time = datetime.datetime.now()



        def on_login(api, ):
            cache_settings = api.settings
            with open(self.settings_file, 'w') as outfile:
                json.dump(cache_settings, outfile, default=to_json)
                print('SAVED: {0!s}'.format(self.settings_file))

        try:
            with open(self.settings_file) as file_data:
                settings = json.load(file_data, object_hook=from_json)
                print('Reusing settings: {0!s}'.format(self.settings_file))

            self.api = API(
                username=username,
                password=password,
                # cookie=load(self.cookie_file),
                on_login=on_login,
                proxy=proxy,
                settings=settings,
            )

        except (ClientCookieExpiredError, ClientLoginRequiredError) as e:
            print('ClientCookieExpiredError/ClientLoginRequiredError: {0!s}'.format(e))
            self.api = API(
                username=username,
                password=password,
                proxy=proxy,
                device_id=settings.get('device_id'),
                on_login=on_login
            )

        self.logger = self.api.logger

        self.total = TOTAL
        self.delay = DELAY
        self.max_per_day = MAX_PER_DAY

        # methods used in propertis used in yaml
        self._followers_ids = []
        self._followers_usernames = []
        self._following_ids = []
        self._following_usernames = []

        # self.api.login()



    def __repr__(self):
        return 'Bot(username=\'{}\', id={})'.format(self.username, self.id)


    def relogin(self):
        self.api.login()


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



def make_cookie_file( file, name):
    if not file:
        file = Path(str(Path('.') / '_cookies' / name)).resolve()
        file.parent.exists() or file.parent.mkdir()
    file = Path(file)
    file.exists() or file.touch()
    return str(file.resolve())


def make_file( file, name, initial=''):
    if not file:
        file = Path(str(Path('.') / name)).resolve()
        file.parent.exists() or file.parent.mkdir()
    file = Path(file)
    if not file.exists():
         file.touch()
         with open(str(file.resolve()), 'w') as f:
             f.write(initial)
    return str(file.resolve())


def make_settings_file( file, name):
    if not file:
        file = Path(str(Path('.') / '_settings' / name)).resolve()
        file.parent.exists() or file.parent.mkdir()
    file = Path(file)
    file.exists() or file.touch()
    return str(file.resolve())



def load(path):
    with open(path) as f:
        return f.read()
