from instagram_private_api import Client, ClientCookieExpiredError, ClientLoginRequiredError
from colorlog import ColoredFormatter
import logging
import os



class LoggerAdapter(logging.LoggerAdapter):
    def __init__(self, logger, prefix):
        super(LoggerAdapter, self).__init__(logger, {})
        self.prefix = prefix

    def process(self, msg, kwargs):
        return '[%s] %s' % (self.prefix, msg), kwargs


class API(Client):
    def __init__(self,**kwargs):
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
            
            
    def _prepare_recipients(users, thread_id=None, use_quotes=False):
        if not isinstance(users, list):
            print('Users must be an list')
            return False
        result = {'users': '[[{}]]'.format(','.join(users))}
        if thread_id:
            template = '["{}"]' if use_quotes else '[{}]'
            result['thread'] = template.format(thread_id)
        return result


    def send_direct_item(self, users, **options):
        data = {
            'client_context': self.generate_uuid(),
            'action': 'send_item'
        }

        url = 'direct_v2/threads/broadcast/{}/'.format(item_type)
        text = options.get('text', '')
        
        if options.get('urls'):
            data['link_text'] = text
            data['link_urls'] = json.dumps(options.get('urls'))
            
        elif options.get('media_id',) and options.get('media_type'):
            data['text'] = text
            data['media_type'] = options.get('media_type', 'photo')
            data['media_id'] = options.get('media_id', '')
            
        elif options.get('hashtag',):
            data['text'] = text
            data['hashtag'] = options.get('hashtag', '')
            
        elif options.get('profile_user_id'):
            data['text'] = text
            data['profile_user_id'] = options.get('profile_user_id')
            
        else:
            data['text'] = text

        data['recipient_users'] = f"[[{','.join(users)}]]"
        if options.get('thread'):
            data['thread_ids'] = f'[{options.get('thread')}]'
        data.update(self.authenticated_params)
        return self._call_api(url, params=data, unsignature=True)

  


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
