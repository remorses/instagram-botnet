
import os
from .support import *


def test_scrape_chain():
    template = """
    actions:
        -
            name: 1
            nodes: [instagram]
            from: user
            edges:
                - followers:
                    amount: 2
                - scrape:
                    model: x.username
                    key: users
    ---
    actions:
        -
            name: 1
            nodes: {{ users }}
            from: user
            edges:
                - follow
    """
    assert os.getenv('username')
    data = dotdict(
        username=os.getenv('username'),
        password=os.getenv('password'),
        settings_path=os.getenv('username')+'_settings.json'
    )
    result = execute(template, data)
    print(json.dumps(result, indent=4))


def test_complex_eval():
    template = """
    bot:
        username: {{ env.username }}
        password: {{ env.password }}
        settings_path: {{ env.username + '_settings.json' }}
    actions:
        -
            name: 1
            nodes: {{
                list(
                    set(['xmorse_']) |
                    set([])
                )
            }}
            from: user
            edges:
                - followers:
                    amount: 5
                - scrape:
                    model: x.username
                    key: users
    
    """
    data = dotdict()
    result = execute(template, data)
    print(json.dumps(result, indent=4))