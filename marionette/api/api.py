
from instabot import API as NOT_MY_API
from instabot.api import config, devices
from colorlog import ColoredFormatter
import logging
from .html_log import HTMLFileHandler, HTMLFormatter


class API(NOT_MY_API):

    def __init__(self, log_path, device=None, id=''):
        self.id = id
        # Setup device and user_agent
        device = device or devices.DEFAULT_DEVICE
        self.device_settings = devices.DEVICES[device]
        self.user_agent = config.USER_AGENT_BASE.format(**self.device_settings)

        self.is_logged_in = False
        self.last_response = None
        self.total_requests = 0

        # Setup logging

        fh = HTMLFileHandler(title=self.id, file=log_path, mode='w')
        fh.setLevel(logging.INFO)
        fh.setFormatter(file_formatter())

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(colred_formatter())

        self.logger = logging.getLogger('[{}]'.format(self.id))
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)
        self.logger.setLevel(logging.DEBUG)

        self.last_json = None


def colred_formatter():
    format = '%(asctime)s | %(levelname)8s | %(message)s'
    cformat = '%(log_color)s' + format
    date_format = '%Y-%m-%d h%H'
    return ColoredFormatter(cformat, date_format,
                            log_colors={'DEBUG': 'reset',       'INFO': 'green',
                                        'WARNING': 'yellow', 'ERROR': 'red',
                                        'CRITICAL': 'red'})


def file_formatter():
    format = '%(asctime)s | %(levelname)-8s | %(message)s'
    cformat = '%(log_color)s' + format
    date_format = '%Y-%m-%d h%H'
    return HTMLFormatter(cformat, date_format,)
