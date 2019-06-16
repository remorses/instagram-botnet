import datetime
from pathlib import Path
import time
from ..api import API
from ..api.instagram_private_api import  (
    ClientError,
    ClientLoginRequiredError,
    ClientCookieExpiredError,
    ClientConnectionError,
    ClientThrottledError,
    ClientLoginError,
    ClientReqHeadersTooLargeError,
    ClientCheckpointRequiredError,
    ClientChallengeRequiredError,
    ClientSentryBlockError,
)
from .support import to_json, from_json, serialize_cookie_jar
from .settings import DELAY, TOTAL, MAX_PER_DAY
import json
import portalocker
import os
import logging


class Bot:

    id = 0

    def __init__(
                 self,
                 username,
                 password,
                 # cookie_file=None,
                 settings_path=None,
                 settings=None,
                 proxy=None,
                 device=None,
                 max_per_day={},
                 latitude=0,
                 longitude=0,
                 filter_predicates=[],
                 delay={},
                 disable_logging=False,
                 script_name='not named script',
                 log_level='INFO',
                 ):
        

        # TODO this is horrible
        if settings_path and not settings:
            self.settings_file = make_file(settings_path, username + '_settings.json', initial='{}')
            with open(self.settings_file, 'r') as file_data:
                settings = json.load(file_data, )
                print('Reusing settings: {0!s}'.format(self.settings_file))
        elif settings is not None:
            self.settings_file = None
        else:
            raise Exception('neither settings or settings_file present')

        # self.id = Bot.id
        self.username = username
        
        self.password = password
        self.proxy = proxy
        self.predicates = filter_predicates or []
        self.total = TOTAL
        self.delay = {**DELAY, **delay}
        self.latitude = latitude or 0
        self.longitude = longitude or 0
        self.max_per_day = {**MAX_PER_DAY, **max_per_day}
        self.script_name = script_name

        

        self.start_time = datetime.datetime.utcnow()



        def on_login(api: API, ):
            nonlocal settings
            settings.update({**settings, **api.settings})
            cookies = api.opener.cookie_jar._cookies
            cookies = serialize_cookie_jar(cookies)
            settings['cookies'] = cookies
            del settings['cookie']
            if self.settings_file:
                with portalocker.Lock(self.settings_file, 'w', timeout=10) as outfile:
                    json.dump(settings, outfile, default=to_json, indent=4)
                    print('SAVED: {0!s}'.format(self.settings_file))
                    outfile.flush()
                    os.fsync(outfile.fileno())
            

        try:
            self.api = API(
                username=username,
                password=password,
                on_login=on_login,
                proxy=proxy,
                settings=settings,
            )
            if not settings.get('cookies'):
                self.api.do_login()

        except (ClientCookieExpiredError, ClientLoginRequiredError, ClientLoginError, ClientConnectionError) as e:
            print('ClientCookieExpiredError/ClientLoginRequiredError: {0!s}'.format(e))
            self.api = API(
                username=username,
                password=password,
                proxy=proxy,
                settings=settings.update({'cookies': {}}),
                on_login=on_login
            )
            self.api.do_login()
        self.logger = self.api.logger

        self.logger.setLevel(getattr(logging, log_level))

        if disable_logging:
            self.logger.setLevel(logging.CRITICAL)
            
        if os.getenv('DEBUG'):
            self.logger.setLevel(logging.DEBUG)
        

        # self.api.login()



    def __repr__(self):
        return 'Bot(username=\'{}\')'.format(self.username)


    def relogin(self):
        self.api.do_login()


    def reached_limit(self, key):
        current_date = datetime.datetime.now()
        passed_days = (current_date.date() - self.start_time.date()).days
        if passed_days > 0:
            self._reset_counters()
        return self.max_per_day[key] - self.total[key] < 0

    @property
    def metadata(self):
        return {
            'username': self.username,
            'pk': str(self.pk),
            'proxy': self.proxy,
            'lng': float(self.longitude),
            'lat': float(self.latitude),
            'start_time': str(self.start_time),
            'script_name': self.script_name,
            # 'action_name': self.action_name,
            # 'totals': self.total,
        }

    @property
    def pk(self):
        return self.api.authenticated_user_id
    

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




def load(path):
    with open(path) as f:
        return f.read()
