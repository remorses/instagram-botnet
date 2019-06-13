from funcy import ignore, raiser, rcompose
from random import choice
from ..bot import Bot
from .common import decorate, substitute_vars, tap
from ..nodes import Comment, Media, User, Geotag




@decorate(accepts=Media, returns=Media)
def comment(bot: Bot, nodes,  args):

    try:
        max = float(args['max']) if 'max' in args else float('inf')
        comments = args['comments']
    except Exception:
        bot.logger.error('please add all necessary args, {} isn\'t enought'.format(args))
        return [], {}

    count = 0



    def increment():
        nonlocal count
        count += 1

    stop = raiser(StopIteration)



    return_if_suitable = lambda node: node \
        if bot.suitable(node, table='commented', specifier=str(comments)) \
        else tap(None,lambda: bot.logger.warning('{} not suitable'.format(node)))

    discard_if_reached_limit = lambda node: node \
        if not bot.reached_limit('comments') \
        else tap(None, bot.logger.error('reached commenting daily limit'))

    do_comment_from_groups = lambda node: map(
            lambda cmnts: do_comment(bot, choice(cmnts), node),
            comments) and node \
         if node else None



    process = rcompose(
        lambda x: stop() if x and count >= max else x,
        # return_if_suitable,
        # discard_if_reached_limit,
        do_comment_from_groups,
        lambda x: tap(x, increment) if x else None,
    )


    result = map(process, nodes)
    result = filter(lambda x: x, result)

    return result, {}




def do_comment(bot: Bot, text, node, thread_id=None):

    media_id = node.pk
    # print('caption', node.caption._yaml())
    evaluated_text = substitute_vars(text,
        author=ignore(Exception, '')(
            lambda: User(**node.user).username
        )(),
        # caption=node['caption']['text'],
        geotag=ignore(Exception, '')(
            lambda: Geotag(**node.location).name or ''
        )(),
        usertags=ignore(Exception, '')(
            lambda: list(map(lambda x: User(**x), node._usertags)) or []
        )()
    )

    bot.api.post_comment(
        media_id=media_id,
        comment_text=evaluated_text,
    )

    bot.logger.info('commented %s' % node)
    bot.total['comments'] += 1
    bot.sleep('comment')
    return node
