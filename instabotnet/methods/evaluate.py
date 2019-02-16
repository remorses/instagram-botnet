import traceback
from ..nodes import Node
from .common import accepts


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
            bot.logger.error('there was an error:\n{}'.format(traceback.format_exc()))
            bot.sleep('error')
            pass
        else:
            count += 1
            bot.logger.info(f'{int(count / total * 100)}%: evaluated {count} nodes of {total} total')

    # bot.logger.warn(nodes[:3])

    return nodes, {}
