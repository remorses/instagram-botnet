from .common import accepts
from ..nodes import Node, User, Media
from ..debug import unmask
from .common import today, tap, dotdict
from ..bot import Bot
from dataset import connect
from funcy import rcompose, ignore, retry
import time



@accepts(Node)
def scrape(bot: Bot, nodes,  args):

    try:
        amount = args['amount'] or float('inf')
        database = args['database']
        table = args['table']
        model = args['model']

    except KeyError as exc:
        bot.logger.error('please add all necessary args, {}'.format( exc))
        return [], {}


    count = 0

    def increment():
        nonlocal count
        count += 1

    lazy_database = lambda: connect(
        database,
        engine_kwargs = {'connect_args': {'check_same_thread' : False}}
    )

    with lazy_database() as db:
        for node in nodes:
            """
            model:
                name:      x.full_name
                id:        x.pk
                followers: x.followers_count
            """
            insertion = dotdict()
            for name, expr in model.items():
                insertion[name] = evaluate(expr, node, bot=bot)

            if count <= amount:
                db[table].insert(insertion)
                bot.logger.info('added to database node {} with insertion {}'.format(node, insertion))
                increment()
            else:
                 break

    return [], bot.last



def evaluate(expr, node, bot):
    x = node._data or node.get_data(bot)
    x = dotdict(**x)
    value = xeval(expr, x)
    if not value:
        x = node.get_data(bot)
        x = dotdict(**x)
        return xeval(expr, x)
    else:
        return value

def xeval(expr, x):
    try:
        return eval(expr, dotdict(x=x))

    except (KeyError, AttributeError):
        return None
