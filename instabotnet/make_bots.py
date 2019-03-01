from .make_predicate import make_predicate
from .bot import Bot





def make_bots(script):
    """


    bots:
        -
            username:           '{username}'
            password:           qwerty
            cache:              ./cache.db
            log:                ./logs.html
            cookie:             ./cookie.json
        -
            username:           giovanotti
            password:           qwerty
            cache:              ./cache.db
            log:                ./logs.html
            cookie:             ./cookie.json

    bot:
        username: sds
        password: ...

    max_per_day:
        likes:                  50
        follow:                 20
        unfollow:               10
        ...

    delay:
        like:                   10
        usual:                  2
        ...

    """

    bots = []

    if 'bots' in script:
        for data in script['bots']:
            bot = Bot(**params(data))
            if 'latitude' in data and 'longitude' in data:
                bot.latitude = data['latitude']
                bot.longitude = data['bot']['longitude']
            bots += [bot]

    elif 'bot' in script:
        data = script['bot']
        bot = Bot(**params(data))
        if 'latitude' in data and 'longitude' in data:
            bot.latitude = data['latitude']
            bot.longitude = data['bot']['longitude']
        bots += [bot]

    else:
        raise Exception('no bots in script')

    for bot in bots:
        modify_bot(bot, data)


    return bots

def error(exception):
    raise exception



params = lambda data: dict(
        cookie_file=data['cookie'] if 'cookie' in data else None,
        username=data['username'] if 'username' in data \
            else error(Exception('username necessary')),
        password=data['password'] if 'password' in data \
            else error(Exception('password necessary')),
    )

def modify_bot(bot, script):
        if 'max_per_day' in script:
            bot.max_per_day = {key: value for key,
                               value in script['max_per_day'].items()}
        if 'delay' in script:
            bot.delay = {**bot.delay, **{key: value for key, value in script['delay'].items()} }

        if 'filter' in script:
            bot.predicates += [make_predicate(script['filter'], bot)]
