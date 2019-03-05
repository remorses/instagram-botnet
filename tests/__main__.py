import sys
from . import credentials
import time
import os.path
sys.path.append( os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from instabotnet import execute
import yaml
import json

def load(path):
    with open(path) as f:
        return f.read()


tests = [
    # 'tests/basic.yml',
    # 'tests/upload_single_post.yml',
    # 'tests/upload_carousel_post.yml',
    # 'tests/upload_video_post.yml',
    # 'tests/delete_last_post.yml',
    # 'tests/print_user_stories.yml',
    # 'tests/scrape_users.yml',
    # 'tests/print_users_feed.yml',
    'tests/message_some_urls.yml',
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

    data = execute(
        load(path),
        {
            'USERNAME': credentials.USER,
            'username': credentials.USER,
            'PASSWORD': credentials.PASS,
            'password': credentials.PASS,
            'settings': open(credentials.USER + '_settings.json').read()
            'competitors': ['instagram'],
            'inspirations': ['archillect.png'],
            'hashtags': ['pizza'],
            'geotags': ['monaco'],
            'proxy': None,
            
        }
    )
    # print(yaml.dump(data, Dumper=Dumper, default_flow_style=False))
    print(json.dumps(data, indent=4))
    time.sleep(3)
