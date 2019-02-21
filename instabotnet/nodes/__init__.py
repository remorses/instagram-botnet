
from .node import Node
from .user import User
from .hashtag import Hashtag
from .geotag import Geotag
from .arg import Arg
from .media import Media
from .story import Story
from .comment import Comment

node_classes = dict(
    node=Node,
    user=User,
    media=Media,
    story=Story,
    hashtag=Hashtag,
    geotag=Geotag,
    arg=Arg,
    comment=Comment,
)

(node_classes,)