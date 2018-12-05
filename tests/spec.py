import sys
from pathlib import Path
import json
import subprocess

sys.path += [str(Path(__file__).parents[1])]
from marionette import execute, prepare
from tests.parse import parse


def unmask(obj):
    data = json.dumps(obj)
    cmd = 'echo {0!r} | unmask-json --stream --raw'.format(data)
    print(cmd)

    ps = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = ps.communicate()[0]

    # out = subprocess.check_output(
    #     [cmd ], shell=True, stderr=subprocess.PIPE)

    return out.decode('ascii')

################################################################################


SCRIPTS = [
    parse('tests/like.yml'),
    parse('tests/authors.yml'),
]

################################################################################

data = {}
for script in SCRIPTS:
    bots = prepare(script)
    data[script['name']] = execute(script, bots)


print('________________________________________________________________________')
print('')

for name, raw in data.items():

    with open('tests/outputs/{}.json'.format(name), 'w') as file:
        file.write(json.dumps(raw, indent=4 ))

    with open('tests/outputs/{}.graphql'.format(name), 'w') as file:
        file.write(unmask(raw))
