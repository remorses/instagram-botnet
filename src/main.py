from .bot import Bot

workers = {}
script = {}


class Task():
    def __init__(self, bot, id):
        self._bot = bot
        self.acc = bot.acc
        self.id = id


for i, credentials in enumerate(script['bots']):
    workers[i] = Task(Bot(**credentials), id=i)


threads = []

if 'distributed' in script['mode']:

    for action in script['execute']:

        method, options = action.items()[0]

        if 'nodes' in options:

            for i, node in options['nodes']:
                workers[i % len(workers)].acc += [node]

            for i, worker in workers:
                worker.bot.start(options['nodes'], method,
                                 worker.bot.acc, **options)

            for i, worker in workers.items():
                worker.bot.acc.clear()

        elif 'from_nodes' in options:

            for i, node in enumerate(options['from_nodes']):
                workers[i % len(workers)].bot.acc += [node]

            for i, worker in workers.items():
                for edge in options['via_edges']:
                    threads.append(workers[i].bot.start(
                        method, workers[i].bot.acc, **options))

                for t in threads:
                    t.join()

                for i, worker in workers.items():
                    worker.bot.acc.clear()

elif 'unison' in script['mode']:
    pass
