from .common import decorate
from ..nodes import Media
from ..bot import Bot



@decorate(accepts=Media, returns=Media)
def delete(bot: Bot, nodes,  args):


    for node in nodes:
        res = bot.api.delete_media(node.id)

        if not res.get('did_delete'):
            bot.logger.warning(f'can\'t delete media {node}')
        else:
            bot.logger.info(f'deleted {node}')

        bot.sleep('delete')


    return [], {}
