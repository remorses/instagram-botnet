#!/bin/bash

cd "$( dirname ${BASH_SOURCE[0]})"
cd ..
python -m tests.spec
