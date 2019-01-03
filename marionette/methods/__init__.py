from functools import partial
from .like import like
from .follow import follow
from .authors import authors
from .followers import followers
from .following import following
from .user_feed import user_feed
from .hashtag_feed import hashtag_feed
from .likers import likers
from .hashtags import hashtags
from .usertags import usertags
from .geotag import geotag
from .geotag_feed import geotag_feed

methods = dict(
               authors=authors,
               followers=followers,
               likers=likers,
               following=following,
               user_feed=user_feed,
               hashtag_feed=hashtag_feed,
               hashtags=hashtags,
               usertags=usertags,
               geotag=geotag,
               geotag_feed=geotag_feed,

               follow=follow,
               like=like,
              )

#
# def make_methods(bot):
#     return {key: partial(value, bot) for (key, value) in methods.items()}
