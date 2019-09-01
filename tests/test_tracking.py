from instabotnet import execute
import os
import json
from .support import dotdict
from mock_api import track_method
from .templates import all



def test_1():
    with track_method('instabotnet.api.instagram_private_api.client.Client', '_call_api', 'api.yaml', arg=1):
        for name, template in all.items():
            print(f'running {name}')
            print(template)
            result = execute(template, dotdict(os.environ))
            print(json.dumps(result, indent=4))
