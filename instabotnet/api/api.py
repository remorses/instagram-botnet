from instagram_private_api import Client
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
        self.logger = logging.getLogger(__name__)

        # fh = HTMLFileHandler(title=self._id, file=logs_file, mode='w')
        # fh.setLevel(logging.INFO)
        # fh.setFormatter(file_formatter())
        # self.logger.addHandler(fh)

        ch = logging.StreamHandler()
        ch.setLevel(get_logging_level())
        ch.setFormatter(colred_formatter())
        self.logger.addHandler(ch)

        self.logger.setLevel(logging.DEBUG)
        self.logger = LoggerAdapter(self.logger, kwargs['username'])



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