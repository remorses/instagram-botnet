
from ruamel.yaml import YAML

yaml = YAML()

def load_yaml(path):
    with open(path) as f:
        return yaml.load(f.read())