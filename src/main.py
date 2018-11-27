from .bot.bot import Bot

bots = []
script = {}
threads = []


for i, credentials in enumerate(script['bots']):
    bots[i] = Bot(**credentials)


def wait_bots(threads):
    for t in threads:
        t.join()


class ScriptException(Exception):
    pass


if 'distributed' in script['mode']:

    for action in script['execute']:

        method, options = action.items()[0]

        if 'nodes' in options:

            for i, node in options['nodes']:
                bots[i % len(bots)].acc += [node]

            for bot in bots:
                threads.append(bot.start(method,
                                         bot.acc, options['args']))

            wait_bots(threads)

        elif 'from_nodes' in options:

            for i, node in enumerate(options['from_nodes']):
                bots[i % len(bots)].acc += [node]

            # scrape the nodes from edges relations
            if 'via_edges' in options:

                for edge in options['via_edges']:

                    for bot in bots:

                        threads.append(bot.start(
                            edge, bot.acc, options['args']))

                    wait_bots(threads)
            else:
                raise ScriptException(
                    'script using from_nodes must also use via_edges, in action {}'.format(action))

            # execute the final action: like, follow ...
            for bot in bots:

                threads.append(bot.start(
                    method, bot.acc, options['args']))

            wait_bots(threads)

        else:
            raise ScriptException(
                'script action must use at least nodes or from_nodes options, in action {}'.format(action))

elif 'unison' in script['mode']:
    pass
