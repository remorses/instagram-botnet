
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
