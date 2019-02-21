from .common import decorate
from ..nodes import Media




@decorate(accepts=Media, returns=Media)
def delete(bot, nodes,  args):


    for node in nodes:

        if 'instagram.com' in node.url:
            try:
                media_id = node.id
                bot.api.media_info(media_id)
                media = bot.last['items'][0]
                if not bot.api.delete_media(media):
                    bot.logger.warn('deletion didn\'t go well')
            except (KeyError, TypeError):
                bot.logger.warn('cannot delete media {}'.format(node.url))

        else:
            raise Exception('`delete` needs urls of photos to delete')

        bot.logger.debug('sleeping some time')
        bot.sleep('delete')


    return [], {}
