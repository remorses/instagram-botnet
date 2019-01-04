
from instabot import API as NOT_MY_API
from instabot.api import config, devices
from colorlog import ColoredFormatter
import logging
from .html_log import HTMLFileHandler, HTMLFormatter

class LoggerAdapter(logging.LoggerAdapter):
    def __init__(self, logger, prefix):
        super(LoggerAdapter, self).__init__(logger, {})
        self.prefix = prefix

    def process(self, msg, kwargs):
        return '[%s] %s' % (self.prefix, msg), kwargs

class API(NOT_MY_API):

    id = 0

    def __init__(self, logs_file, device=None, username=None,  id=None):

        self.id = API.id if not id else id
        API.id += 1
        # Setup device and user_agent
        device = device or devices.DEFAULT_DEVICE
        self.device_settings = devices.DEVICES[device]
        self.user_agent = config.USER_AGENT_BASE.format(**self.device_settings)

        self.is_logged_in = False
        self.last_response = None
        self.total_requests = 0

        # Setup logging

        fh = HTMLFileHandler(title=self.id, file=logs_file, mode='w')
        fh.setLevel(logging.INFO)
        fh.setFormatter(file_formatter())

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(colred_formatter())

        self.logger = logging.getLogger('[{}]'.format(self.id))
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

        self.logger.setLevel(logging.DEBUG)
        self.logger = LoggerAdapter(self.logger, username)



        self.last_json = None



    def get_story_feed(self, user_id):
        """
        last_json will have the form:
        {
            reel:
                items: {
                ...
                }
                id
                user
                expiring_at
                location
                reel_type
                title
                ...
            }
        }
        """
        url = "feed/user/{user_id}/story/".format(user_id=user_id)
        return self.send_request(url)


def colred_formatter():
    format = '%(asctime)s | %(levelname)-8s | %(message)s'
    cformat = '%(log_color)s' + format
    date_format = '%Y-%m-%d %H:%M'
    return ColoredFormatter(cformat, date_format,
                            log_colors={'DEBUG': 'reset', 'INFO': 'green',
                                        'WARNING': 'yellow', 'ERROR': 'red',
                                        'CRITICAL': 'red'})


def file_formatter():
    format = '%(asctime)s | %(levelname)-8s | %(message)s'
    cformat = '%(log_color)s' + format
    date_format = '%Y-%m-%d %H:%M'
    return HTMLFormatter(cformat, date_format,)
