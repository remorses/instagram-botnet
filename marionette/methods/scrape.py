from .common import accepts
from ..nodes import Node, User, Media
from ..debug import unmask
from .common import today, tap
from ..bot import Bot
from dataset import connect
from funcy import rcompose, raiser, tap as _tap
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
        global count
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
            insertion = dict()
            for name, expr in model.items():
                insertion[name] = evaluate(expr, node, bot=bot)

            if count <= amount:
                db[table].insert(insertion)
                increment()
            else:
                 break

    return [], bot.last



def evaluate(expr, node, bot):
    x = node._data or node.get_data(bot)
    try:
        value = eval(expr, dict(x=x))
        if value:
            return value
        else:
            x = node.get_data(bot)
            value = eval(expr, dict(x=x))
            return value

    except KeyError:
        return True
