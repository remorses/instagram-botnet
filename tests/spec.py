import sys
from pathlib import Path
import json


sys.path += [str(Path(__file__).resolve().parents[1])]
from marionette import execute, prepare
from tests.parse import parse
from tests.unmask import unmask





################################################################################

SCRIPTS = [
    # parse('./hashtags.yml'),
    # parse('./geotag_feed.yml'),
    # parse('./geotag.yml'),
    # parse('./usertags.yml'),
    # parse('./like.yml'),
    # parse('./authors.yml'),
    # parse('./hashtag_feed.yml'),
    # parse('./followers.yml'),
    # parse('./user_feed.yml'),
    parse('./likers.yml'),
    # parse('./complex.yml'),
    # parse('./upload.yml'),
    # parse('./delete.yml'),

]

################################################################################

data = {}
for script in SCRIPTS:
    bots = prepare(script)
    data[script['name']] = execute(script, bots)




for name, raw in data.items():

    ok = False

    with open('./artifacts/{}.json'.format(name), 'w+') as file:
        content = file.read()
        json = json.dumps(raw, indent=4)
        if len(raw) > len(json):
            ok = True
            file.write(data)
        else:
            file.write(content)

    with open('./artifacts/{}.graphql'.format(name), 'w+') as file:
        content = file.read()

        if ok:
            file.write(unmask(raw))
        else:
            file.write(content)
