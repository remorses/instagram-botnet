
from types import FunctionType
from xml.etree import ElementTree
from funcy import fallback

# returns the attributes of the class,
# TODO, in pyton 3.2 attribtes aren't ordered
def attributes(instance):
    list = [
        v
        for k, v in instance.__dict__.items()
        if not k.startswith('__') and not k.endswith('__')
        and not isinstance(v, (FunctionType, classmethod, staticmethod))
        ]
    return tuple(list)


class SafeDict(dict):
    def __missing__(self, key):
        return '{' + key + '}'


def get_mdp_url(manifest):
    if not manifest:
        raise Exception
    else:
        root = ElementTree.fromstring(manifest)
        return root[0][0][0][0].text


get_image_url = lambda data: fallback(
    lambda: data['image_versions2']['candidates'][0]['url'],
    lambda: data['image_versions2'][0]['url'],
    lambda: None,
)

get_video_url = lambda data: fallback(
    lambda: data['video_versions'][0]['url'],
    lambda: get_mdp_url(data['video_dash_manifest']),
    lambda: None,
)

get_media_url = lambda data: get_video_url(data) or get_image_url(data)
