

from support import *


def test_message():
    template = """
    bot:
        username: {{ env.username }}
        password: {{ env.password }}
        settings_path: {{ env.username + '_settings.json' }}
    actions:
        -
            name: 1
            nodes: [xmorse_]
            from: user
            edges:
                - follow
                - message:
                    messages:
                        - [ciao]
                    
    """
    data = dotdict()
    result = execute(template, data)
    print(json.dumps(result, indent=4))

def test_scrape():
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
                - follow
    """
    data = dotdict()
    result = execute(template, data)
    print(json.dumps(result, indent=4))

def test_like():
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
                - feed:
                    amount: 1
                - like
    """
    data = dotdict()
    result = execute(template, data)
    print(json.dumps(result, indent=4))

