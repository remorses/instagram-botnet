from functools import partial
from .nodes import Media, User
from .bot import Bot


def prepare(script):

    bots = make_bots(script)

    for bot in bots:
        if 'filter' in script:
            # has_filter = bot.username in data['only'] or not data['only']
            bot.predicates += [make_predicate(script['filter'], bot)]

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


def make_predicate(script, bot):
    """
    filter:

        user:
                followers:      x > 50 and x < 1000
                following:      x < 500
                bio:            any(s not in ['porn', 'sex'] for s in x)
                is_private:     x and False
                is_business:    x and False
                is_verified:    x and False

        media:
                likers:         x < 1000
                hastags:        any(s not in ['porn', 'sex'] for s in x)
                likes:          x < 200
                comments:       x < 100
                caption:        any(s not in ['porn', 'sex'] for s in x)
                # geotag not
                # usertag not

        geotag:
                name:           any(s not in {{ cities }} for s in x)
                lat:            x < 1000 and x > 500
                lng:            x < 1000 and x > 500

        usertag:                true


    """
    def predicate(node):

        bool = True

        if isinstance(node, Media):
             pass
        elif isinstance(node, User):
             bool = bool and check(script['user']['followers'], node.get_followers_count(bot))
             bool = bool and check(script['user']['following'], node.get_following_count(bot))
             bool = bool and check(script['user']['bio'], node.get_bio(bot))
             bool = bool and check(script['user']['is_private'], node.get_is_private(bot))
             bool = bool and check(script['user']['is_business'], node.get_is_business(bot))
             bool = bool and check(script['user']['is_verified'], node.get_is_verified(bot))

        else:
            return True

        return bool

    return predicate


def check(expr, var):
    return eval(expr, dict(x=var))
