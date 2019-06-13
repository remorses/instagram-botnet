import os
import traceback
from ..nodes import Node, node_classes
from .common import decorate
from ..api.instagram_private_api.errors import (
    ClientError,
    ClientLoginRequiredError,
    ClientCookieExpiredError,
    ClientConnectionError,
    ClientThrottledError,
    ClientReqHeadersTooLargeError,
)
from ..bot import Bot
from ..handle_errors import handle



DEBUG = bool(os.environ.get('DEBUG'))

@decorate(accepts=(*node_classes.values(),), returns=Node)
def evaluate(bot: Bot, nodes,  args) -> Node:

    total = args['info']['total_nodes']
    count = 0
    nodes = iter(nodes)


    while True:
        try:
            res = handle(lambda: next(nodes), bot)
        except StopIteration:
            break
        except Exception as e:
            # bot.logger.error(f'unexpected exception {e}')
            raise e from None
        else:
            count += 1
            percentage = (str(int(count / total * 100)) + '%').center(5)
            bot.logger.info( f'{percentage}:  {count} nodes out of {total}')

        


    # bot.logger.warning(nodes[:3])

    return nodes, {}




# try:
#             next(nodes)

#         except StopIteration:
#             break

#         except ClientLoginRequiredError as e:
#             bot.logger.error(str(e))
#             bot.relogin()

#         except ClientConnectionError as e:
#             bot.logger.error(str(e))

#         except (ClientReqHeadersTooLargeError, ClientThrottledError) as e:
#             bot.logger.error(str(e))
#             bot.sleep(5 * 60)

#         except ClientError as e: # when trying to see private user
#             bot.logger.error(str(e))
#             bot.sleep()

#         except Exception as e:
#             bot.logger.error('unexpected exception {e}')
#             raise e from None