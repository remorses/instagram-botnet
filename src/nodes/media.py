
from funcy import rcompose
from .common import attributes
from .node import Node
from .user import User
from .geotag import Geotag
from .hashtag import Hashtag
import time

class Media(Node):

    def __init__(self, *, generic=False, url=False, id=False, data={}):

        self._url = url
        self._id = id
        self._data = data

        if generic:
            self._url = generic

    def __repr__(self):
        url, id, data = attributes(self)
        if url:
            return 'Media(url=\'{}\')'.format(url)
        elif id:
            return 'Media(id={})'.format(id)
        elif data:
            return 'Media(data=\'{...}\')'

    @property
    def id(self):
        url, id, data = attributes(self)
        if id:
            return id
        elif url:
            return id_from_url(url)
        else:
            raise Exception('can\'t retrieve id, not enought data')

    @property
    def url(self):
        url, id, data = attributes(self)
        if url:
            return url
        elif id:
            return url_from_id(id)
        elif data:
            return data['media_id']
        else:
            raise Exception
    @property
    def data(self,):

        if self.id:
            bot = self._bot
            bot.api.media_info(id)
            bot.sleep('usual')
            if 'items' in bot.last:
                self._data = bot.last["items"][0]
                return self._data

        elif self.url:
            id = id_from_url(self.url)
            self._id = id
            return self.data

        else:
            return {}

    @property
    def author(self,):
        data = self._data
        if 'user' in data:
            user = data["user"]
            return User(
                data=user,
                id=user['pk'],
                username=user['username']
            )
        else:
            data = self.data
            user = data["user"]
            return User(
                data=user,
                id=user['pk'],
                username=user['username']
            )
    @property
    def like_count(self,):
        data = self._data
        if 'like_count' in data:
            return data['like_count']
        else:
            data = self.data
            return data['like_count']
    @property
    def comment_count(self,):
        data = self._data
        if 'comment_count' in data:
            return data['comment_count']
        else:
            data = self.data
            if 'comment_count' in data:
                return data['comment_count']
            else:
                return False
    @property
    def caption(self,):
        data = self._data
        if 'caption' in data:
            return data['caption']['text']
        else:
            if 'location' in data:
                data = self.data
                return data['caption']['text']
            else:
                return False
    @property
    def geotag(self,):
        data = self._data
        if 'location' in data:
            return data['location']
        else:
            data = self.data
            if 'location' in data:
                return  Geotag(
                    name=data['name'],
                    id=data['pk'],
                    data=data
                )
            else:
                return False

    @property
    def usertags(self,):
        data = self._data
        pack_user = rcompose(
            lambda data: data['user'],
            lambda data: User(username=data['username'], id=data['pk'], data=data)
        )

        try:
            if 'usertags' in data:
                items =  data["usertags"]["in"]
                yield from (pack_user(item) for item in items)
            else:
                data = self.data
                if 'usertags' in data:
                    items =  data["usertags"]["in"]
                    yield from (pack_user(item) for item in items)
                else:
                    return False
        except KeyError:
            return False



    def hashtags(self,):
        text = self.caption
        raw_tags = set(part[1:] for part in text.split() if part.startswith('#'))
        tags = (Hashtag(name=tag) for tag in raw_tags)
        yield from tags

















def id_from_url(link):
    if 'instagram.com/p/' not in link:
        # self.logger.error('Unexpected link')
        return False
    link = link.split('/')
    code = link[link.index('p') + 1]

    alphabet = {
        '-': 62, '1': 53, '0': 52, '3': 55, '2': 54, '5': 57, '4': 56,
        '7': 59, '6': 58, '9': 61, '8': 60, 'A': 0, 'C': 2, 'B': 1,
        'E': 4, 'D': 3, 'G': 6, 'F': 5, 'I': 8, 'H': 7, 'K': 10, 'J': 9,
        'M': 12, 'L': 11, 'O': 14, 'N': 13, 'Q': 16, 'P': 15, 'S': 18,
        'R': 17, 'U': 20, 'T': 19, 'W': 22, 'V': 21, 'Y': 24, 'X': 23,
        'Z': 25, '_': 63, 'a': 26, 'c': 28, 'b': 27, 'e': 30, 'd': 29,
        'g': 32, 'f': 31, 'i': 34, 'h': 33, 'k': 36, 'j': 35, 'm': 38,
        'l': 37, 'o': 40, 'n': 39, 'q': 42, 'p': 41, 's': 44, 'r': 43,
        'u': 46, 't': 45, 'w': 48, 'v': 47, 'y': 50, 'x': 49, 'z': 51,
        }

    result = 0
    for char in code:
        result = result * 64 + alphabet[char]
    return result


def url_from_id(id):
    id = int(id)
    alphabet = {
        '-': 62, '1': 53, '0': 52, '3': 55, '2': 54, '5': 57, '4': 56,
        '7': 59, '6': 58, '9': 61, '8': 60, 'A': 0, 'C': 2, 'B': 1,
        'E': 4, 'D': 3, 'G': 6, 'F': 5, 'I': 8, 'H': 7, 'K': 10, 'J': 9,
        'M': 12, 'L': 11, 'O': 14, 'N': 13, 'Q': 16, 'P': 15, 'S': 18,
        'R': 17, 'U': 20, 'T': 19, 'W': 22, 'V': 21, 'Y': 24, 'X': 23,
        'Z': 25, '_': 63, 'a': 26, 'c': 28, 'b': 27, 'e': 30, 'd': 29,
        'g': 32, 'f': 31, 'i': 34, 'h': 33, 'k': 36, 'j': 35, 'm': 38,
        'l': 37, 'o': 40, 'n': 39, 'q': 42, 'p': 41, 's': 44, 'r': 43,
        'u': 46, 't': 45, 'w': 48, 'v': 47, 'y': 50, 'x': 49, 'z': 51,
        }
    result = ''
    while id:
        id, char = id // 64, id % 64
        result += list(alphabet.keys())[list(alphabet.values()).index(char)]
    return 'https://instagram.com/p/' + result[::-1] + '/'
