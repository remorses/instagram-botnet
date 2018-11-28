import sys
import os
from pathlib import Path
sys.path += [str(Path(__file__).parents[1])]

from marionette import execute


import yaml


threads = []

with open("tests/example.yaml", 'r') as stream:
    try:
        execute(yaml.load(stream), threads)
    except yaml.YAMLError as exc:
        print('error: ', exc)
