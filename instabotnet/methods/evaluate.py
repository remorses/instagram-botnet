import os
from ..nodes import Node
from .common import accepts

DEBUG = bool(os.environ.get('DEBUG'))

@accepts(Node)
def evaluate(bot, nodes,  args) -> Node:

    total = args['info']['total_nodes']
    count = 0

    while True:

        try:

            try:
                next(nodes)

            except TypeError:
                next(iter(nodes))

        except StopIteration:
            break
        except:
            raise
        else:
            count += 1
            percentage = (str(int(count / total * 100)) + '%').center(5)
            bot.logger.info( f'{percentage}:  {count} nodes out of {total}')

    # bot.logger.warn(nodes[:3])

    return nodes, {}
