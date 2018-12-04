import sys
from pathlib import Path
import json
import subprocess

sys.path += [str(Path(__file__).parents[1])]
from marionette import execute, prepare
from tests.parse import parse


def unmask(obj):
    data = json.dumps(obj)
    cmd = 'echo {0!r} | unmask-json --stream  '.format(data),
    ps = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = ps.communicate()[0]

    # out = subprocess.check_output(
    #     [cmd ], shell=True, stderr=subprocess.PIPE)

    return out.decode('ascii')

################################################################################


SCRIPTS = [
    # parse('tests/like.yml'),
    parse('tests/authors.yml'),
]

################################################################################

data = {}
for script in SCRIPTS:
    bots = prepare(script)
    data[script['name']] = execute(script, bots)


print(json.dumps(data))
print('________________________________________________________________________')
print('')
print(unmask(data))
