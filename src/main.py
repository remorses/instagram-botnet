from .bot import Bot

workers = {}
script = {}


class Task():
    def __init__(self, bot, id):
        self.bot = bot
        self.acc = bot.acc
        self.id = id


for i, credentials in enumerate(script['bots']):
    workers[i] = Task(Bot(**credentials), id=i)

threads = []


def wait_bots(threads):
    for t in threads:
        t.join()


if 'distributed' in script['mode']:

    for action in script['execute']:

        method, options = action.items()[0]

        if 'nodes' in options:

            for i, node in options['nodes']:
                workers[i % len(workers)].acc += [node]

            for i, worker in workers.items():
                threads.append(worker.bot.start(method,
                                                worker.acc, options['args']))

            wait_bots(threads)

        elif 'from_nodes' in options:

            for i, node in enumerate(options['from_nodes']):
                workers[i % len(workers)].acc += [node]

            # scrape the nodes from edges relations
            if 'via_edges' in options:

                for edge in options['via_edges']:

                    for i, worker in workers.items():

                        threads.append(worker.bot.start(
                            edge, worker.acc, options['args']))

                    wait_bots(threads)
            else:
                raise Exception(
                    'script using from_nodes must also use via_edges, in action {}'.format(action))

            # execute the final action: like, follow ...
            for i, worker in workers.items():

                threads.append(worker.bot.start(
                    method, worker.acc, options['args']))

            wait_bots(threads)

        else:
            raise Exception(
                'script action must use at least nodes or from_nodes options, in action {}'.format(action))

elif 'unison' in script['mode']:
    pass
