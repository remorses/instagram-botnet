import logging
import os
import json
import mock
from instabotnet import execute
from .support import dotdict
from mock_api import track_method, mock_method

defaults = {
    'delay': {
        'usual': 0,
        'like': 0,
        'follow': 0,
        'comment': 0,
        'delete': 0,
        'text': 0,
        'error': 0,
        'unfolow': 0,
        'upload': 0,
    },
}



def test_1(template):
    mock.patch('instabotnet.api.API.do_login', new=lambda s: None).start()
    with mock_method('instabotnet.api.instagram_private_api.client.Client', '_call_api', 'api.yaml', arg=1):
        print('running')
        print(template)
        result = execute(template, dotdict({**defaults, **os.environ}))
        print(json.dumps(result, indent=4))

def test_logging_handler(template):
    mock.patch('instabotnet.api.API.do_login', new=lambda s: None).start()
    with mock_method('instabotnet.api.instagram_private_api.client.Client', '_call_api', 'api.yaml', arg=1):
        print('running')
        print(template)
        class FileHandler(logging.Handler):
            terminator = '\n'

            def __init__(self, collection):
                logging.Handler.__init__(self)
                self.collection = collection
            def write_to_db(self, record):
                with open(self.collection, 'a') as f:
                    f.write(record)
            def emit(self, record):
                try:
                    msg = self.format(record)
                    self.write_to_db(msg + '\n')
                except Exception:
                    self.handleError(record)

        result = execute(template, dotdict({**defaults, **os.environ}), handlers=[FileHandler('play_logs.txt')])
        print(json.dumps(result, indent=4))
