
from .author import author
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
from .stories import stories
from .feed import feed
from .sleep import sleep

from .like import like
from .follow import follow
from .unfollow import unfollow
from .message import message
from .upload_post import upload_post
from .comment import comment
from .delete import delete
from .scrape import scrape
from .edit_profile import edit_profile
from .shuffle import shuffle
from .print import _print

from .evaluate import evaluate

methods = dict(
   author=author,
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
   stories=stories,
   feed=feed,
   sleep=sleep,
   follow=follow,
   unfollow=unfollow,
   like=like,
   message=message,
   upload_post=upload_post,
   comment=comment,
   delete=delete,
   edit_profile=edit_profile,
   shuffle=shuffle,
   print=_print,
   scrape=scrape,

   evaluate=evaluate,
)

(methods,)

#
# def make_methods(bot):
#     return {key: partial(value, bot) for (key, value) in methods.items()}
