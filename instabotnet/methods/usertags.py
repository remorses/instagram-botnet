from funcy import mapcat, rcompose
from itertools import islice
from typing import List
from ..nodes import User, Media
from .common import decorate





@decorate(accepts=Media, returns=User)
def usertags(bot, nodes,  args) -> List[User]:

    amount = args.get('amount') or 1


    def process(node,):
        tags = node._usertags
        tags = [User(**data) for data in tags]
        # print(tags)
        yield from islice(tags, amount)

    result = mapcat(process, nodes)

    return result, {}
