import traceback
from ..nodes import Node
from .common import accepts


@accepts(Node)
def evaluate(bot, nodes,  args) -> Node:

    result = []

    while True:
        try:
            result += next(nodes)
        except TypeError:
            result += next(iter(nodes))
        except StopIteration:
            break
        except:
            bot.logger.error('there was an error:\n{}'.format(traceback.format_exc()))
            bot.sleep('error')
            pass

    # bot.logger.warn(nodes[:3])

    return nodes, bot.last
