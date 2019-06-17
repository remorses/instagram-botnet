

from .support import *
import os
# def test_upload():
#     template = """
#     bot:
#         username: {{ env.username }}
#         password: {{ env.password }}
#         settings_path: {{ env.username + '_settings.json' }}
#     actions:
#         -
#             name: 1
#             nodes:
#                 # - 'https://images1.apartments.com/i2/nKi28WK6ehLQFaC7840rel_Yj1KkegXMz6vtF7iyhZM/111/panorama-tower-miami-fl-primary-photo.jpg'
#                 - 'https://www.instagram.com/p/BxkxjB-HQ0v/'
#             from: media
#             edges:
#                 - upload_post:
#                     max: 1
#                     caption: weila
#                     geotag: colorado
                    
#     """
#     data = dotdict()
#     result = execute(template, data)
#     print(json.dumps(result, indent=4))





def test_proxy():
    template = """
    log_level: DEBUG

    actions:
        -
            name: 1
            nodes: [{{ username }}]
            from: user
            edges:
                - followers:
                    amount: 1
                - scrape:
                    key: mine
                    model: x.username
    """
    assert os.getenv('username')
    data = {
        'username': os.getenv('username'),
        'password': os.getenv('password'),
        # 'settings': {},
        'proxy': os.getenv('proxy'),
        'settings_path': os.getenv('username') + '_settings.json',
        'to_mutate': 1,
    }
    result = execute(template, data)
    print(json.dumps(result, indent=4))

def test_sleep():
    template = """
    log_level: DEBUG

    actions:
        -
            name: 1
            nodes: [{{ username }}]
            from: user
            edges:
                - sleep: 10
                - followers:
                    amount: 1
                - scrape:
                    key: mine
                    model: x.username
    """
    assert os.getenv('username')
    data = {
        'username': os.getenv('username'),
        'password': os.getenv('password'),
        'settings': {},
        'to_mutate': 1,
    }
    result = execute(template, data)
    print(json.dumps(result, indent=4))


def test_edit():
    template = """
    disable_logging: true

    actions:
        -
            name: 1
            nodes: [{{ env.username }}]
            from: user
            edges:
                - edit_profile:
                    first_name: Magic Mark
                    gender: MALE
                    email: asdasd@fuckclubs.club
                    privacy: private
                    biography: imma good guy
                    profile_picture: 'https://upload.wikimedia.org/wikipedia/en/9/95/Test_image.jpg'
                    external_url: google.com
                - scrape:
                    key: edited
                    model: "{**x}"
    _: {{ data.update({'to_mutate': 0}) }}
    """
    data = {
        'username': os.getenv('username'),
        'password': os.getenv('password'),
        'settings': {},
        'to_mutate': 1,
    }
    result = execute(template, data)
    print(json.dumps(result, indent=4))
    assert data['to_mutate'] == 0
    




def test_empty():
    template = """
    """
    data = {}
    result = execute(template, data)
    print(json.dumps(result, indent=4))
    


def test_private_follow():
    template = """
    bot:
        username: {{ env.username }}
        password: {{ env.password }}
        settings_path: {{ env.username + '_settings.json' }}
    actions:
        -
            name: 1
            nodes: [patelvaibhav6992]
            from: user
            edges:
                - feed:
                    amount: 1
                - like
    """
    data = dotdict()
    result = execute(template, data)
    print(json.dumps(result, indent=4))
    

def test_scrape_all():
    template = """
    bot:
        username: {{ env.username }}
        password: {{ env.password }}
        settings_path: {{ env.username + '_settings.json' }}
    actions:
        -
            name: 1
            nodes: [mongodb]
            from: user
            edges:
                - followers:
                    amount: 2
                - scrape:
                    model: x.username
                    key: users
    """
    data = dotdict()
    result = execute(template, data)
    print(json.dumps(result, indent=4))


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
                    amount: 2
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



