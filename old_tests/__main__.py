import sys

import time
import os.path
sys.path.append( os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from instabotnet import execute
import yaml
import json

class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def load(path):
    with open(path) as f:
        return f.read()

try:
    from . import credentials

except Exception:
    class credentials:
        USER = os.environ.get('IG_USERNAME')
        PASS = os.environ.get('IG_PASSWORD')



tests = [
    # 'tests/basic.yml',
    # 'tests/upload_single_post.yml',
    # 'tests/upload_carousel_post.yml',
    # 'tests/upload_video_post.yml',
    # 'tests/delete_last_post.yml',
    # 'tests/print_user_stories.yml',
    # 'tests/scrape_users.yml',
    'tests/print_users_feed.yml',
    # 'tests/message_some_urls.yml',
    # 'tests/repost_routine.yml',
]



class Dumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(Dumper, self).increase_indent(flow, False)

for path in tests:
    print()
    print()
    print()
    print()
    print()
    print()
    config = dotdict(**{
            'USERNAME': credentials.USER,
            'username': credentials.USER,
            'PASSWORD': credentials.PASS,
            'password': credentials.PASS,
            # 'settings': json.load(open(credentials.USER + '_settings.json', 'r')),
            'settings_path': credentials.USER + '_settings.json',
            'competitors': ['instagram'],
            'inspirations': ['archillect.png'],
            'captions': ['hey', 'bruh'],
            'hashtags': ['pizza'],
            'geotags': ['monaco'],
            'comments': ['wow', 'awesome'],
            'proxy': None,

    })
    data = execute(
        load(path),
        config
    )
    # print('data: \n', yaml.dump(data, Dumper=Dumper, default_flow_style=False))

    print('returned data:')
    print(json.dumps(dict(**data), indent=4))
    print('config:')
    print(json.dumps(config, indent=4))
    time.sleep(3)
