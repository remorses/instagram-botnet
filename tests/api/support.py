from dotenv import load_dotenv

load_dotenv()

import os
class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

env = dotdict(os.environ)

import json

from instabotnet import execute, async_execute

import pytest

from instabotnet import Bot
from instabotnet.nodes import Media, User

log = lambda x: print(json.dumps(x, indent=4))