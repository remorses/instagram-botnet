from functools import partial

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
from .filter import filter
from .user_stories import user_stories

from .like import like
from .follow import follow
from .unfollow import unfollow
from .text import text
from .upload import upload
from .comment import comment
from .delete import delete
from .scrape import scrape
from .set_profile import set_profile
from .shuffle import shuffle
from .print import _print

from .evaluate import evaluate

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
   filter=filter,
   user_stories=user_stories,

   follow=follow,
   unfollow=unfollow,
   like=like,
   text=text,
   upload=upload,
   comment=comment,
   delete=delete,
   scrape=scrape,
   set_profile=set_profile,
   shuffle=shuffle,
   print=_print,

   evaluate=evaluate,
)

#
# def make_methods(bot):
#     return {key: partial(value, bot) for (key, value) in methods.items()}
