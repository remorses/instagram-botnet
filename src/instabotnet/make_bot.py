from .make_predicate import make_predicate
from .bot import Bot
from random import random
import json



def make_bot(script, settings):
    """

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
    

    if not 'bot' in script:
        raise Exception('no bot in script')
    data = script['bot']
    bot = Bot(
        settings_path=data['settings_path'] if 'settings_path' in data else None,
        settings=settings or data['settings'] if 'settings' in data else None, # TODO: here i use the settings from variables to be able to mutate it 
        username=data['username'] if 'username' in data else error(Exception('username necessary')),
        password=data['password'] if 'password' in data else error(Exception('password necessary')),
        latitude= data['latitude'] if 'latitude' in data and 'longitude' in data else 0,
        longitude= data['longitude'] if 'latitude' in data and 'longitude' in data else 0,
        max_per_day= {key: value for key, value in script['max_per_day'].items()} if 'max_per_day' in script else {},
        # filter_predicates= [make_predicate(script['filter'], bot)] if 'filter' in script else [], # TODO should not take bot as arg
        delay={key: value for key, value in script['delay'].items()} if 'delay' in script else {},
    )

    if not 'latitude' in script['bot'] or not 'longitude' in script['bot']:
            bot.logger.warn('no latitude and longitude in script, geotag searches will probably fail')

    return bot

def error(exception):
    raise exception





