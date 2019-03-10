from .nodes import Media, User, Geotag, Hashtag

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
    def check(lazy_expr, lazy_var):
        try:
            expr = lazy_expr()
            var = lazy_var()
            result = eval(expr, dict(x=var, bot=bot))
            # print("{} == {} for x={}".format(expr, result, var))
            return result

        except (KeyError, AttributeError):
            # bot.logger.error('failed to check expression')
            return True

    def predicate(node, **kwargs):


        bool = True

        if isinstance(node, Media):
            bool = bool and check(
                lambda: script['media']['likes'],
                lambda: node.get_like_count(bot)
            )
            bool = bool and check(
                lambda: script['media']['comments'],
                lambda: node.get_comment_count(bot)
            )
            bool = bool and check(
                lambda: script['media']['hashtags'],
                lambda: node.get_hashtags(bot)
            )
            bool = bool and check(
                lambda: script['media']['caption'],
                lambda: node.get_caption(bot)
            )
        elif isinstance(node, User):
            bool = bool and check(
                lambda: script['user']['id'],
                lambda: node.get_id(bot)
            )
            bool = bool and check(
                lambda: script['user']['followers'],
                lambda: node.get_followers_count(bot)
            )
            bool = bool and check(
                lambda: script['user']['following'],
                lambda: node.get_following_count(bot)
            )
            bool = bool and check(
                lambda: script['user']['bio'],
                lambda: node.get_bio(bot)
            )
            bool = bool and check(
                lambda: script['user']['is_private'],
                lambda: node.get_is_private(bot)
            )
            bool = bool and check(
                lambda: script['user']['is_business'],
                lambda: node.get_is_business(bot)
            )
            bool = bool and check(
                lambda: script['user']['is_verified'],
                lambda: node.get_is_verified(bot)
            )
        elif isinstance(node, Geotag):
            bool = bool and check(
                lambda: script['geotag']['name'],
                lambda: node.name
            )
            bool = bool and check(
                lambda: script['geotag']['lat'],
                lambda: node.get_coordinates(bot)[0])
            bool = bool and check(
                lambda: script['geotag']['lng'],
                lambda: node.get_coordinates(bot)[1]
            )
        elif isinstance(node, Hashtag):
            bool = bool and check(
                lambda: script['hashtag']['name'],
                lambda: node.name
            )

        else:
            return True

        if not bool:
            bot.logger.debug('{} not suitable, very sorry'.format(node))

        return bool

    return predicate
