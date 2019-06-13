from funcy import raiser, rcompose
from .common import decorate, tap
from ..nodes import Media
from datetime import datetime



@decorate(accepts=Media, returns=Media)
def like(bot, nodes,  args):
    max = float(args['max']) if 'max' in args else float('inf')

    count = 0
    events = []

    def increment():
        nonlocal count
        count += 1
        return True

    def add_event(node: Media):
        events.append({
            'type': 'like',
            'metadata': bot.metadata,
            'node': {
                'type': 'media',
                'url': node.url,
            },
            'timestamp': str(datetime.utcnow())
        })
        return node

    stop = raiser(StopIteration)

    process = rcompose(
        lambda x: stop() if x and count >= max else x,
        # lambda node: node \
        #     if bot.suitable(node) \
        #     else tap(None,lambda: bot.logger.warning('{} not suitable'.format(node))),
        lambda node: like_media(node, bot=bot) \
            if node else None,
        lambda x: x and increment() and x,
        lambda x: x and add_event(x),
    )


    liked = map(process, nodes)
    liked = filter(lambda x: x, liked)

    return liked, { 'events': events }


def like_media(media, bot):
        bot.api.post_like(media.pk)
        bot.logger.info(f'liked media {media}')
        bot.total['likes'] += 1
        bot.sleep('like')
        return media
