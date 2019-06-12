
from .support import *


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
                    amount: 6
                - filter:
                    # username: "'a' not in x"
                    follower_count: x <= 1000
                - feed:
                    amount: 1
                - filter:
                    caption.text: len(x) > 3
                    like_count: x < 2000
                - scrape:
                    key: urls
                    model: x.url
    """
    data = dotdict()
    result = execute(template, data)
    print(json.dumps(result, indent=4))
