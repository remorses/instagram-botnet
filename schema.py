from enum import Enum
from dataclasses import dataclass
from typing import Any, Optional, List


class LogLevel(Enum):
    DEBUG = "DEBUG"
    ERROR = "ERROR"
    INFO = "INFO"


@dataclass
class Root:
    delay: Any
    max_per_day: Any
    disable_logging: Optional[bool] = None
    log_level: Optional[LogLevel] = None
    name: Optional[str] = None
    proxy: Optional[str] = None


@dataclass
class Bot:
    password: str
    settings: Any
    username: str
    latitude: Optional[float] = None
    longitute: Optional[float] = None
    settings_path: Optional[str] = None


class NodeType(Enum):
    ARG = "arg"
    COMMENT = "comment"
    GEOTAG = "geotag"
    HASHTAG = "hashtag"
    MEDIA = "media"
    USER = "user"


@dataclass
class MediaFilter:
    caption: Optional[str] = None
    comments: Optional[str] = None
    likes: Optional[str] = None


class EdgeType(Enum):
    AUTHOR = "author"
    COMMENT = "comment"
    DELETE = "delete"
    FEED = "feed"
    FILTER = "filter"
    FOLLOW = "follow"
    FOLLOWERS = "followers"
    FOLLOWING = "following"
    GEOTAG = "geotag"
    HASHTAGS = "hashtags"
    LIKE = "like"
    LIKERS = "likers"
    PRINT = "print"
    SCRAPE = "scrape"
    SHUFFLE = "shuffle"
    SLEEP = "sleep"
    STORIES = "stories"
    TEXT = "text"
    UNFOLLOW = "unfollow"
    UPLOAD_POST = "upload_post"


@dataclass
class UserFilter:
    biography: Optional[str] = None
    followers: Optional[str] = None
    following: Optional[str] = None
    is_business: Optional[str] = None
    is_private: Optional[str] = None
    is_verified: Optional[str] = None


@dataclass
class Edge:
    model: Any
    type: EdgeType
    caption: Optional[str] = None
    key: Optional[str] = None
    amount: Optional[float] = None
    messages: Optional[List[List[str]]] = None
    comments: Optional[List[List[str]]] = None
    max: Optional[float] = None
    disable_comments: Optional[bool] = None
    geotag: Optional[str] = None
    seconds: Optional[float] = None
    expr: Optional[str] = None
    batch: Optional[float] = None
    media: Optional[MediaFilter] = None
    user: Optional[UserFilter] = None


@dataclass
class ActionElement:
    edges: List[Edge]
    actions_from: NodeType
    name: str
    nodes: List[str]


class UtilityEdgeType(Enum):
    FILTER = "filter"
    PRINT = "print"
    SHUFFLE = "shuffle"
    SLEEP = "sleep"


@dataclass
class UtilityEdge:
    type: UtilityEdgeType
    seconds: Optional[float] = None
    expr: Optional[str] = None
    batch: Optional[float] = None
    max: Optional[float] = None
    media: Optional[MediaFilter] = None
    user: Optional[UserFilter] = None


class GenericEdgeType(Enum):
    AUTHOR = "author"
    FEED = "feed"
    FOLLOWERS = "followers"
    FOLLOWING = "following"
    GEOTAG = "geotag"
    HASHTAGS = "hashtags"
    LIKERS = "likers"
    STORIES = "stories"


@dataclass
class GenericEdge:
    type: GenericEdgeType
    amount: Optional[float] = None


class GenericInteractionEdgeType(Enum):
    DELETE = "delete"
    FOLLOW = "follow"
    LIKE = "like"
    UNFOLLOW = "unfollow"


@dataclass
class GenericInteractionEdge:
    type: GenericInteractionEdgeType
    max: Optional[float] = None


class SleepEdgeType(Enum):
    SLEEP = "sleep"


@dataclass
class SleepEdge:
    seconds: float
    type: SleepEdgeType


class PrintEdgeType(Enum):
    PRINT = "print"


@dataclass
class PrintEdge:
    expr: str
    type: PrintEdgeType


class ScrapeEdgeType(Enum):
    SCRAPE = "scrape"


@dataclass
class ScrapeEdge:
    key: str
    model: Any
    type: ScrapeEdgeType
    max: Optional[float] = None


class ShuffleEdgeType(Enum):
    SHUFFLE = "shuffle"


@dataclass
class ShuffleEdge:
    batch: float
    type: ShuffleEdgeType
    max: Optional[float] = None


class TextEdgeType(Enum):
    TEXT = "text"


@dataclass
class TextEdge:
    messages: List[List[str]]
    type: TextEdgeType
    max: Optional[float] = None


class CommentEdgeType(Enum):
    COMMENT = "comment"


@dataclass
class CommentEdge:
    comments: List[List[str]]
    type: CommentEdgeType
    max: Optional[float] = None


class UploadPostEdgeType(Enum):
    UPLOAD_POST = "upload_post"


@dataclass
class UploadPostEdge:
    type: UploadPostEdgeType
    caption: Optional[str] = None
    disable_comments: Optional[bool] = None
    geotag: Optional[str] = None
    max: Optional[float] = None


class FilterEdgeType(Enum):
    FILTER = "filter"


@dataclass
class FilterEdge:
    type: FilterEdgeType
    media: Optional[MediaFilter] = None
    user: Optional[UserFilter] = None
