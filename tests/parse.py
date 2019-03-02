import yaml


def parse(path):
    with open(path, 'r') as stream:
        try:
            return yaml.load(stream)
        except yaml.YAMLError as exc:
            print('YAML error: ', exc)

def load(path):
    with open(path, 'r') as stream:
        return stream.read()
