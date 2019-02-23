import os
import traceback
from ..nodes import Node, node_classes
from .common import decorate
from ..api.exceptions import (
    LoginRequired,
    TooManyRequests,
    NotFound,
    HeadersTooLarge,
    EmptyResponse,
)

DEBUG = bool(os.environ.get('DEBUG'))

@decorate(accepts=(*node_classes.values(),), returns=Node)
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
            
        except LoginRequired:
            log_error(bot.logger)
            bot.relogin()
            
        except (NotFound, HeadersTooLarge, EmptyResponse):
            log_error(bot.logger)
            bot.sleep()
        
        except TooManyRequests:
            log_error(bot.logger)
            bot.sleep('error')
            
        except:
            raise
            
        else:
            count += 1
            percentage = (str(int(count / total * 100)) + '%').center(5)
            bot.logger.info( f'{percentage}:  {count} nodes out of {total}')

    # bot.logger.warn(nodes[:3])

    return nodes, {}


def log_error(logger):
    logger.error(traceback.format_exc())