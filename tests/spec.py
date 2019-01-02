import sys
from pathlib import Path
import json
import subprocess
from random import random

sys.path += [str(Path(__file__).resolve().parents[1])]
from marionette import execute, prepare
from tests.parse import parse


def unmask(obj):
    data = json.dumps(obj)
    temp_file = temporary_file('temp_' + str(random()), data)

    with temp_file.open('w') as file:
        file.write(data)

    cmd = 'cat {0!s} | unmask-json --stream --raw'.format(temp_file)

    ps = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    out = ps.communicate()[0]

    # temp_file.unlink()

    # out = subprocess.check_output(
    #     [cmd ], shell=True, stderr=subprocess.PIPE)

    return out.decode('ascii')

def temporary_file(name, content):

    cache_path = Path(__file__).parent / '_temp'

    file = Path(str(cache_path.resolve()) + '/' + name + '_temporary')

    file.parent.exists() or file.parent.mkdir()
    file.exists() or file.touch()

    return file.resolve()

################################################################################

print(Path(__file__))
SCRIPTS = [
    # parse('./like.yml'),
    # parse('./authors.yml'),
    # parse('./hashtag_feed.yml'),
    # parse('./followers.yml'),
    # parse('./user_feed.yml')
    parse('./likers.yml')
]

################################################################################

data = {}
for script in SCRIPTS:
    bots = prepare(script)
    data[script['name']] = execute(script, bots)




for name, raw in data.items():

    with open('./outputs/{}.json'.format(name), 'w') as file:
        file.write(json.dumps(raw, indent=4 ))

    with open('./outputs/{}.graphql'.format(name), 'w') as file:
        file.write(unmask(raw))
