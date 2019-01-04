from functools import partial
from .nodes import Media, User, Geotag, Usertag, Hashtag
from .bot import Bot


def prepare(script):

    bots = make_bots(script)

    for bot in bots:
        if 'filter' in script:
            bot.predicates += [make_predicate(script['filter'], bot)]

    return bots


def make_bots(script):
    """
    max_per_day:
        likes:          50
        follow:         20
        unfollow:       10
        ...

    delay:
        likes:          10
        usual:          2
        ...

    """

    bots = []

    for i, credentials in enumerate(script['bots']):
        bots += [Bot(**credentials)]

    for bot in bots:
        if 'max_per_day' in script:
            bot.max_per_day = {key: value for key,
                               value in script['max_per_day'].items()}
        if 'delay' in script:
            bot.delay = {key: value for key, value in script['delay'].items()}

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
            likes:          x < 200
            comments:       x < 100
            caption:        any(s not in x for s in ['porn', 'sex'])

        hashtag:
            name:           not in [porn, sex]

        geotag:
            name:           not in {{ cities }}
            lat:            x < 1000 and x > 500
            lng:            x < 1000 and x > 500


    """
    def predicate(node):

        bool = True

        if isinstance(node, Media):
            bool = bool and check(script['media']['likes'], node.get_like_count(bot))
            bool = bool and check(script['media']['comments'], node.get_comment_count(bot))
            bool = bool and check(script['media']['hashtags'], node.get_hashtags(bot))
            bool = bool and check(script['media']['caption'], node.get_caption(bot))
        elif isinstance(node, User):
            bool = bool and check(script['user']['followers'], node.get_followers_count(bot))
            bool = bool and check(script['user']['following'], node.get_following_count(bot))
            bool = bool and check(script['user']['bio'], node.get_bio(bot))
            bool = bool and check(script['user']['is_private'], node.get_is_private(bot))
            bool = bool and check(script['user']['is_business'], node.get_is_business(bot))
            bool = bool and check(script['user']['is_verified'], node.get_is_verified(bot))
        elif isinstance(node, Geotag):
            bool = bool and check(script['geotag']['name'], node.name)
            bool = bool and check(script['geotag']['lat'], node.get_coordinates(bot)[0])
            bool = bool and check(script['geotag']['lng'], node.get_coordinates(bot)[1])
        elif isinstance(node, Hashtag):
            bool = bool and check(script['hashtag']['name'], node.name)

        else:
            return True

        return bool

    return predicate


def check(expr, var):
    return eval(expr, dict(x=var))
