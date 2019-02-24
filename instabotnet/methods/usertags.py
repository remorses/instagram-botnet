from funcy import mapcat
from typing import List
from ..nodes import User, Media
from .common import decorate





@decorate(accepts=Media, returns=User)
def usertags(bot, nodes,  args) -> List[User]:

    pack_user = rcompose(
        lambda data: data['user'],
        lambda data: User(username=data['username'], id=data['pk'], data=data)
    )

    def get_usertags(node):

        try:
            if 'usertags' in data:
                items =  data["usertags"]["in"]
                yield from (pack_user(item) for item in items)
                
            else:
                yield from []
                
        except KeyError:
            return False

    process = lambda media: get_usertags(media)
    result = mapcat(process, nodes)

    return result, {}



