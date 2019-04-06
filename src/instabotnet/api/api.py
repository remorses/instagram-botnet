from instagram_private_api import (
    Client,
    ClientCookieExpiredError,
    ClientLoginRequiredError,
    ClientError,
    ClientLoginError
)
from ..bot.support import deserialize_cookie_jar
from colorlog import ColoredFormatter
import logging
import os
import json
from instagram_private_api.http import ClientCookieJar


class LoggerAdapter(logging.LoggerAdapter):
    def __init__(self, logger, prefix):
        super(LoggerAdapter, self).__init__(logger, {})
        self.prefix = prefix

    def process(self, msg, kwargs):
        return '[%s] %s' % (self.prefix, msg), kwargs

Client.login = lambda self: None

class API(Client):
    def __init__(self,**kwargs):

        if 'settings' in kwargs and 'cookies' in kwargs['settings']:
            cookies = kwargs['settings']['cookies']
            jar = ClientCookieJar()
            jar._cookies = deserialize_cookie_jar(cookies)
            kwargs['settings']['cookie'] = jar.dump()
            if not 'uuid' in kwargs['settings']:
                kwargs['settings']['uuid'] = self.generate_uuid(False, seed=kwargs['username'])

        super().__init__(**kwargs)

        # Setup logging
        self.logger = logging.getLogger(kwargs.get('username',''))

        # fh = HTMLFileHandler(title=self._id, file=logs_file, mode='w')
        # fh.setLevel(logging.INFO)
        # fh.setFormatter(file_formatter())
        # self.logger.addHandler(fh)
        if not len(self.logger.handlers):
            ch = logging.StreamHandler()
            ch.setLevel(get_logging_level())
            ch.setFormatter(colred_formatter())
            self.logger.addHandler(ch)

            self.logger.setLevel(logging.DEBUG)
            self.logger = LoggerAdapter(self.logger, kwargs['username'])

    def login(self):
        return

    def do_login(self):
        """Login."""

        prelogin_params = self._call_api(
            'si/fetch_headers/',
            params='',
            query={'challenge_type': 'signup', 'guid': self.generate_uuid(True)},
            return_response=True)

        if not self.csrftoken:
            raise ClientError(
                'Unable to get csrf from prelogin.',
                error_response=self._read_response(prelogin_params))

        login_params = {
            'device_id': self.device_id,
            'guid': self.uuid,
            'adid': self.ad_id,
            'phone_id': self.phone_id,
            '_csrftoken': self.csrftoken,
            'username': self.username,
            'password': self.password,
            'login_attempt_count': '0',
        }

        login_response = self._call_api(
            'accounts/login/', params=login_params, return_response=True)

        if not self.csrftoken:
            raise ClientError(
                'Unable to get csrf from login.',
                error_response=self._read_response(login_response))

        login_json = json.loads(self._read_response(login_response))

        if not login_json.get('logged_in_user', {}).get('pk'):
            raise ClientLoginError('Unable to login.')

        if self.on_login:
            on_login_callback = self.on_login
            on_login_callback(self)

    def send_direct_item(self, users, **options):
        data = {
            'client_context': self.generate_uuid(),
            'action': 'send_item'
        }

        users = [str(x) for x in users]

        text = options.get('text', '')

        if options.get('urls'):
            data['link_text'] = text
            data['link_urls'] = json.dumps(options.get('urls'))
            item_type = 'link'

        elif options.get('media_id',) and options.get('media_type'):
            data['text'] = text
            data['media_type'] = options.get('media_type', 'photo')
            data['media_id'] = options.get('media_id', '')
            item_type = 'media_share'

        elif options.get('hashtag',):
            data['text'] = text
            data['hashtag'] = options.get('hashtag', '')
            item_type = 'hashtag'

        elif options.get('profile_user_id'):
            data['text'] = text
            data['profile_user_id'] = options.get('profile_user_id')
            item_type = 'profile'

        else:
            data['text'] = text
            item_type = 'text'

        url = 'direct_v2/threads/broadcast/{}/'.format(item_type)

        data['recipient_users'] = f"[[{','.join(users)}]]"
        if options.get('thread_id'):
            data['thread_ids'] = f"[{options.get('thread_id')}]"
        data.update(self.authenticated_params)
        return self._call_api(url, params=data, unsigned=True)



    def agree_consent1(self):
        params = {
            '_csrftoken': self.csrftoken,
            '_uid': self.authenticated_user_id,
            '_uuid': self.uuid
        }
        return self._call_api('consent/existing_user_flow/', params=params, )# unsigned=True)


    def agree_consent2(self):
        params = {
            'current_screen_key': 'qp_intro',
            'updates': json.dumps({'existing_user_intro_state': '2'}),
            '_csrftoken': self.csrftoken,
            '_uid': self.authenticated_user_id,
            '_uuid': self.uuid
        }
        return self._call_api('consent/existing_user_flow/', params=params, )# unsigned=True)


    def agree_consent3(self):
        params = {
            'current_screen_key': 'tos_and_two_age_button',
            'updates': json.dumps({'age_consent_state': '2', 'tos_data_policy_consent_state': '2'}),
            '_csrftoken': self.csrftoken,
            '_uid': self.authenticated_user_id,
            '_uuid': self.uuid
        }
        return self._call_api('consent/existing_user_flow/', params=params,)# unsigned=True)




def get_logging_level():
        levels = dict(
            DEBUG=logging.DEBUG,
            INFO=logging.INFO,
            WARN=logging.WARN,
            ERROR=logging.ERROR,
            CRITICAL=logging.CRITICAL,
        )

        return os.environ['LOGGING_LEVEL'] \
            if 'LOGGING_LEVEL' in os.environ and os.environ['LOGGING_LEVEL'] in levels \
            else logging.DEBUG if 'DEBUG' in os.environ else 'INFO'

def colred_formatter():
    format = '%(asctime)s | %(levelname)-8s | %(message)s'
    cformat = '%(log_color)s' + format
    date_format = '%Y-%m-%d %H:%M'
    return ColoredFormatter(cformat, date_format,
                            log_colors={'DEBUG': 'reset', 'INFO': 'green',
                                        'WARNING': 'yellow', 'ERROR': 'red',
                                        'CRITICAL': 'red'})
