import sys
from pathlib import Path
import json
from subprocess import check_output

sys.path += [str(Path(__file__).parents[1])]
from marionette import execute, prepare
from tests.parse import parse


def unmask(obj):
    # cat package.json | unmask-json --stream --indents 0
    data = json.dumps(obj)
    # print('echo {0!r} | unmask-json --stream --indents 0'.format(data))
    out = check_output(
        ['echo {0!r} | unmask-json --stream --indents 0'.format(data), ], shell=True)
    return out.decode('ascii')


scripts = [
    parse('tests/like.yml'),
]

data = {}
for script in scripts:
    bots = prepare(script)
    data[script['name']] = execute(script, bots)

print(unmask(data))
