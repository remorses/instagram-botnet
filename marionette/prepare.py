from functools import partial
from .nodes import Media, User
from .bot import Bot


def prepare(script):

    bots = make_bots(script)

    for bot in bots:
        if 'filter' in script:
            data = script['filter']
            has_filter = bot.username in data['only'] or not data['only']
            bot.filter = make_filter(data) if has_filter else identity

    return bots


def make_bots(script):

    bots = []

    for i, credentials in enumerate(script['bots']):
        bots += [Bot(**credentials)]

    for bot in bots:
        if 'max_per_day' in script:
            bot.max_per_day = {key: value for key,
                               value in script['max_per_day']}
        if 'delay' in script:
            bot.delay = {key: value for key, value in script['delay']}

    return bots


def make_filter(data):
    """
    only:   [bot1, bot2]

    user:
            followers: x > 50 and x < 1000
            following: x < 500
    media:
            likers:    x < 1000
            hastags:   not in ['porn', 'sex']
    """

    def _filter(nodes):
        if is_user(nodes[-1]):
            return filter(partial(user_sieve, data), nodes)

        elif is_media(nodes[-1]):
            return filter(partial(media_sieve, data), nodes)

        else:
            raise Exception

    return _filter


def user_sieve(data, node) -> bool:

    checks = []

    if 'followers' in data:
        checks += [check(data['followers'], node.followers)]
    if 'following' in data:
        checks += [check(data['following'], node.following)]

    return all(checks)


def media_sieve(data, node):
    pass


def check(expr, var):
    return eval(expr, dict(x=var))


def is_user(node):
    return isinstance(node, User)


def is_media(node):
    return isinstance(node, Media)


def identity(*args, **kwargs):
    others = kwargs.values()
    return (*args, *others)
