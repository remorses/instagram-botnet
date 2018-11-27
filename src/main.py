from .bot import Bot

bots = {}
script = {}
distributed = True

if 'mode' in script:
    if script['mode'] != 'distributed':
        distributed = False

for i, credentials in enumerate(script['bots']):
    bots[i] = {'bot': Bot(credentials), 'id': i, 'acc': []}


threads = []

for action in script['execute']:

    method, options = action.items()[0]

    if 'nodes' in options:

        for i, node in options['nodes']:
            bots[i % len(bots)]['bot'].acc += [node]

        for i, bot in bots:
            bot['bot'].start(options['nodes'], method,
                             bot['bot'].acc, **options)

        for i, bot in bots.items():
            bot['bot'].acc.clear()

    elif 'from_nodes' in options:

        for i, node in enumerate(options['from_nodes']):
            bots[i % len(bots)]['bot'].acc += [node]

        for i, bot in bots.items():
            for edge in options['via_edges']:
                threads.append(bots[i]['bot'].start(
                    method, bots[i]['bot'].acc, **options))

            for t in threads:
                t.join()

            for i, bot in bots.items():
                bot['bot'].acc.clear()
