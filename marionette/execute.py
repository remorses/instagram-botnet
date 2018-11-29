from .bot import Bot
import time
from threading import Thread
from random import random


# class Bot:
#
#     idx = 0
#
#     def __init__(self, username, password):
#         Thread.__init__(self)
#         print('init')
#
#         self.acc = []
#         self.id = id
#         Bot.idx += 1
#         self.edges = Edges(self)
#
#     def do(self, method, arg):
#         t = Thread(target=self.edges.like, args=(method, arg))
#         t.start()
#         return t
#
#
# class Edges:
#
#     def __init__(self, bot):
#         self.bot = bot
#         self.idx = bot.idx
#
#     def like(self, method, arg):
#             time.sleep(1)
#             print('{} did {}'.format(self.idx, self.bot.acc))
#             self.bot.acc = [round(random() * 10)]


class ScriptException(Exception):
    pass


def wait(threads):
    for t in threads:
        t.join()
    threads = []


def reset(bots):
    for bot in bots:
        bot.reset()


def execute(script, threads):

    wait(threads)

    bots = []

    for i, credentials in enumerate(script['bots']):
        bots += [Bot(**credentials)]

    if 'distributed' in script['mode']:

        for action in script['execute']:

            interaction_method, options = list(action.items())[0]

            if not 'args' in options:
                options['args'] = []

            if 'nodes' in options:

                reset(bots)

                for i, node in enumerate(options['nodes']):
                    bots[i % len(bots)].accumulate(node)

                for bot in bots:
                    print('bot: ', bot)
                    print('acc: ', bot.acc)
                    threads += [bot.do(interaction_method, options['args'])]

                wait(threads)

            elif 'from_nodes' in options:

                reset(bots)

                for i, node in enumerate(options['from_nodes']):
                    bots[i % len(bots)].accumulate(node)

                # scrape the nodes from edges relations
                if 'via_edges' in options:

                    for edge in options['via_edges']:

                        for bot in bots:
                            threads += [bot.do(edge, options['args'])]

                        wait(threads)
                else:
                    raise ScriptException(
                        'script using from_nodes must also use via_edges, in action {}'.format(action))

                # execute the final interaction: like, follow ...
                for bot in bots:

                    threads.append(bot.do(interaction_method, options['args']))

                wait(threads)

            else:
                raise ScriptException(
                    'script action must use at least nodes or from_nodes options, in action {}'.format(action))

    elif 'unison' in script['mode']:
        pass

    time.sleep(3)
