from .support import *




@pytest.mark.asyncio
async def test_async_scrape():
    template = """
    bot:
        username: {{ env.username }}
        password: {{ env.password }}
        # settings_path: {{ env.username + '_settings.json' }}
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
    bot:
        username: {{ env.username }}
        password: {{ env.password }}
        # settings_path: {{ env.username + '_settings.json' }}
    actions:
        -
            name: 1
            nodes: {{ users }}
            from: user
            edges:
                - follow
    """
    data = dotdict()
    result = await async_execute(template, os.environ,)
    print(json.dumps(result, indent=4))

