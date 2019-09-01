
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
    result = execute(template, env,)
    print(json.dumps(result, indent=4))


def test_chain_works():
    template = """
    bot:
        username: {{ env.username }}
        password: {{ env.password }}
        # settings_path: {{ env.username + '_settings.json' }}
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
                - scrape:
                    model: x.username
                    key: key
    ---
    {{ print(key) }}
    ---
    {{ data.update({'to_mutate': to_mutate + 3})}}
    
    """
    to_mutate = 1
    data = {'to_mutate': to_mutate, **env}
    result = execute(template, data,)
    assert data['to_mutate'] != to_mutate
    print(json.dumps(result, indent=4))