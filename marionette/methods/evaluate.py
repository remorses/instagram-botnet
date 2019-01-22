import traceback
from ..nodes import Node
from .common import accepts


@accepts(Node)
def evaluate(bot, nodes,  args) -> Node:

    result = []

    while True:
        try:
            result += next(nodes)
        except StopIteration:
            break
        except Exception as e:
            bot.logger.error('there was an error:\n{}'.format(traceback.format_exc()))
            pass

    # bot.logger.warn(nodes[:3])

    return nodes, bot.last
