
from instabot import API as NOTMYAPI
from instabot.api import config, devices
import logging
from colorlog import ColoredFormatter
from .html_log import HTMLFileHandler, HTMLFormatter


class API(NOTMYAPI):

    def __init__(self, log_to, device=None, id=''):
        self.id = id
        # Setup device and user_agent
        device = device or devices.DEFAULT_DEVICE
        self.device_settings = devices.DEVICES[device]
        self.user_agent = config.USER_AGENT_BASE.format(**self.device_settings)

        self.is_logged_in = False
        self.last_response = None
        self.total_requests = 0

        # Setup logging

        fh = HTMLFileHandler(title=self.id, filename=log_to, mode='w')
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
    format = '%(asctime)s - %(levelname)-8s - %(message)s'
    cformat = '%(log_color)s' + format
    date_format = '%Y-%m-%d %H'
    return ColoredFormatter(cformat, date_format,
                            log_colors={'DEBUG': 'reset',       'INFO': 'reset',
                                        'WARNING': 'bold_yellow', 'ERROR': 'bold_red',
                                        'CRITICAL': 'bold_red'})


def file_formatter():
    format = '%(asctime)s - %(levelname)-8s - %(message)s'
    cformat = '%(log_color)s' + format
    date_format = '%Y-%m-%d %H'
    return HTMLFormatter(cformat, date_format,)
