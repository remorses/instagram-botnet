from dotenv import load_dotenv

load_dotenv()

import os
class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

env = {**os.environ}

import json

from instabotnet import execute, async_execute

import pytest

