import sys
from pathlib import Path

sys.path += [str(Path(__file__).parents[1])]
from marionette import execute, prepare
from tests.parse import parse


scripts = [
    parse('tests/like.yml'),
]

data = []
for script in scripts:
    bots = prepare(script)
    data += [execute(script, bots)]

print('done', data)
