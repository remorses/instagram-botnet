# from .bot import Bot
import time
from threading import Thread
from random import random


class Bot:

    idx = 0

    def __init__(self, username, password):
        Thread.__init__(self)
        print('init')

        self.acc = []
        self.id = id
        Bot.idx += 1
        self.edges = Edges(self)

    def run(self, method, arg):
        t = Thread(target=self.edges.like, args=(method, arg))
        t.start()
        return t


class Edges:

    def __init__(self, bot):
        self.acc = bot.acc
        self.idx = bot.idx

    def like(self, method, arg):
            time.sleep(1)
            print('{} did {}'.format(self.idx, self.acc))
            self.acc = [(random() * 10) * 100 / 100]


class ScriptException(Exception):
    pass


def wait_bots(threads):
    for t in threads:
        t.join()
    threads.empty()


def execute(script, threads):

    wait_bots(threads)

    bots = []

    for i, credentials in enumerate(script['bots']):
        bots += [Bot(**credentials)]

    if 'distributed' in script['mode']:

        for action in script['execute']:

            method, options = list(action.items())[0]
            if not 'args' in options:
                options['args'] = []

            if 'nodes' in options:

                for i, node in options['nodes']:
                    bots[i % len(bots)].acc += [node]

                for bot in bots:
                    threads.append(bot.run(method, options['args']))

                wait_bots(threads)

            elif 'from_nodes' in options:

                for i, node in enumerate(options['from_nodes']):
                    bots[i % len(bots)].acc += [node]

                # scrape the nodes from edges relations
                if 'via_edges' in options:

                    for edge in options['via_edges']:

                        for bot in bots:

                            threads.append(bot.run(edge, options['args']))

                        wait_bots(threads)
                else:
                    raise ScriptException(
                        'script using from_nodes must also use via_edges, in action {}'.format(action))

                # execute the final action: like, follow ...
                for bot in bots:

                    threads.append(bot.run(method, options['args']))

                wait_bots(threads)

            else:
                raise ScriptException(
                    'script action must use at least nodes or from_nodes options, in action {}'.format(action))

    elif 'unison' in script['mode']:
        pass
