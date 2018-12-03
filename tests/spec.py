import sys
from pathlib import Path
import yaml

sys.path += [str(Path(__file__).parents[1])]
from marionette import execute, prepare


with open("tests/example.yaml", 'r') as stream:
    try:
        script = yaml.load(stream)
    except yaml.YAMLError as exc:
        print('YAML error: ', exc)


bots = prepare(script)

attempt = execute(script, bots=bots)

if attempt:
    print('done')

else:
    error: Exception = attempt
    print(error)
