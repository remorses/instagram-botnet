from .common import decorate
from ..nodes import Node, node_classes
import json
from .common import dotdict
from ..bot import Bot
from funcy import mapcat
import time
from datetime import datetime



@decorate(accepts=(*node_classes.values(),), returns=Node)
def sleep(bot: Bot, nodes,  args):
    try:
        amount = int(args)
    except Exception:
        bot.logger.error('wait argument must be a number (of seconds)')
    time.sleep(amount)

    events = [{
        'type': 'sleep',
        'metadata': bot.metadata,
        'node': {},
        'timestamp': str(datetime.utcnow()),
    }]
    return nodes, { 'events': events }