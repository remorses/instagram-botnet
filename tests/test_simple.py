

from support import *

def test_simple():
    template = """
    bot:
        username: {{ env.username }}
        password: {{ env.password }}
        settings_path: {{ env.username + '.json' }}
    actions:
        -
            name: 1
            nodes: [instagram]
            from: user
            edges:
                - followers:
                    amount: 5
                - scrape:
                    model:
                        username: x.username
                    key: users
    """
    data = dotdict()
    result = execute(template, data)
    print(json.dumps(result, indent=4))

def test_follow():
    template = """
    bot:
        username: {{ env.username }}
        password: {{ env.password }}
        settings_path: {{ env.username + '_settings.json' }}
    actions:
        -
            name: 1
            nodes: [instagram]
            from: user
            edges:
                - followers:
                    amount: 5
                - scrape:
                    model:
                        username: x.username
                    key: users
    """
    data = dotdict()
    result = execute(template, data)
    print(json.dumps(result, indent=4))