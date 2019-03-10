from instabotnet import execute
import os
import yaml
import json

path = os.environ['SCRIPT']

def load(path):
    with open(path) as f:
        return f.read()

class Dumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(Dumper, self).increase_indent(flow, False)

# print(yaml.dump(dict(**os.environ), Dumper=Dumper, default_flow_style=False))

data = execute(
    load(path),
    os.environ
)
print('returned data:')
print(json.dumps(dict(**data), indent=4))
