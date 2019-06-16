import codecs
# from http.cookies import BaseCookie
from ..api.instagram_private_api.compat import compat_cookiejar
def to_json(python_object):
    if isinstance(python_object, bytes):
        return {'__class__': 'bytes',
                '__value__': codecs.encode(python_object, 'base64').decode()}
    raise TypeError(repr(python_object) + ' is not JSON serializable')


def from_json(json_object):
    if '__class__' in json_object and json_object['__class__'] == 'bytes':
        return codecs.decode(json_object['__value__'].encode(), 'base64')
    return json_object


def serialize_cookie(cookie):
    obj = {}
    for name in (
        "version", "name", "value", "port", "port_specified",
        "domain", "domain_specified", "domain_initial_dot",
        "path", "path_specified",
        "secure", "expires", "discard", "comment", "comment_url",
    ):
        obj[name] = getattr(cookie, name)
    return obj

def serialize_cookie_jar(jar, ):
    result={}
    for k, v in jar.items():
        if isinstance(v, compat_cookiejar.Cookie):
            result[k] = serialize_cookie(v)
        elif isinstance(v, dict):
            result[k] = serialize_cookie_jar(v, )
        else:
            result[k] = v
    return result

def deserialize_cookie(cookie):
    obj = {}
    for name in (
        "version", "name", "value", "port", "port_specified",
        "domain", "domain_specified", "domain_initial_dot",
        "path", "path_specified",
        "secure", "expires", "discard", "comment", "comment_url", "rest"
    ):
        obj[name] = cookie.get(name)
    return compat_cookiejar.Cookie(**obj)

def deserialize_cookie_jar(jar):
    result={}
    for k, v in jar.items():
        if 'name' in v and 'version' in v:
            result[k] = deserialize_cookie(v)
        elif isinstance(v, dict):
            result[k] = deserialize_cookie_jar(v, )
        else:
            result[k] = v
    return result
