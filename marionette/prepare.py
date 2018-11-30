from .bot import Bot


def prepare(script, threads=[]):

    bots = []

    for i, credentials in enumerate(script['bots']):
        bots += [Bot(**credentials)]

    for bot in bots:
        if 'max_per_day' in script:
            bot.max_per_day = {
                key: value for key, value in script['max_per_day']}
        if 'delay' in script:
            bot.delay = {key: value for key,
                         value in script['delay']}

    return bots


def wait(threads):
    [t.join() for t in threads]
    threads = []
