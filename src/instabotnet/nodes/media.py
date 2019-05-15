
from funcy import rcompose, ignore, fallback, mapcat
from .node import Node
from .schemas import media_schema
from modeller import Model
from .common import get_image_url, get_manifest, get_video_url
import traceback





class Media(Model, Node):

    def _on_init(self):
        try:
            self._validate()
        except Exception as e:
            print('ERROR in validation for Media:')
            print()
            print(str(e))
            print()
            print(self._yaml())
            print()

    _schema = media_schema

    __repr__ = lambda self: f'Media(url={self.url})'

    # id = property(lambda self: self.pk)

    url = property(lambda self: url_from_id(self.pk))

    # for image data, for video posts returns the thumbnail
    images = property(lambda self:  \
        list(map(get_image_url, self['carousel_media'])) if self['carousel_media'] \
        else [get_image_url(self)] or
        []
    )

    # for videos, it is a MDP, if it is long it needs to be recomposed
    mpd = property(lambda self:  \
        list(map(get_manifest, self['carousel_media'] or [])) if self['carousel_media'] \
        else [get_manifest(self)] or
        []
    )

    videos = property(lambda self:  \
        list(map(get_video_url, self['carousel_media'] or [])) if self['carousel_media'] \
        else [get_video_url(self)] or
        []
    )




    # def fallback(*args):
    #     first = lambda arr: arr[1:] if len(arr) > 0 else lambda: None
    #     rest = lambda arr: arr[:1]if len(arr) > 0 else []
    #     return  first(args)() or fallback(rest(args))

    _usertags = property(lambda self: fallback(
        lambda : self['usertags']['in']['user'],
        lambda : list(map(lambda x: x['user'], self['usertags']['in'])),
        lambda : list(map(lambda x: x['user'], self['caption']['usertags']['in'])),
        lambda: list(mapcat(lambda data: map(lambda x: x['user'], data['usertags']['in']), self['carousel_media'] or [])),
        lambda: list(mapcat(lambda data: map(lambda x: x['user'], data['caption']['usertags']['in']), self['carousel_media'] or [])),
        lambda: []
    ))

    # geotag = property(lambda self: self['location'])


























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
