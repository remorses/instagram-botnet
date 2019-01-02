import sys
from pathlib import Path
import json


sys.path += [str(Path(__file__).resolve().parents[1])]
from marionette import execute, prepare
from tests.parse import parse
from tests.unmask import unmask





################################################################################

SCRIPTS = [
    parse('./like.yml'),
    parse('./authors.yml'),
    parse('./hashtag_feed.yml'),
    parse('./followers.yml'),
    parse('./user_feed.yml'),
    parse('./likers.yml')
]

################################################################################

data = {}
for script in SCRIPTS:
    bots = prepare(script)
    data[script['name']] = execute(script, bots)




for name, raw in data.items():

    with open('./artifacts/{}.json'.format(name), 'w') as file:
        file.write(json.dumps(raw, indent=4 ))

    with open('./artifacts/{}.graphql'.format(name), 'w') as file:
        file.write(unmask(raw))
