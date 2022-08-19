#!/bin/bash

# Clear logs & build files
rm -rf dist/ build/ .nox/ .pytest_cache/ tftools.egg-info/ tests/sponge_log.xml

rm test/sponge_log.xml test/__pycache__ __pycache__

python3 setup.py install

rm -rf dist/ build/ .nox/ .pytest_cache/ tftools.egg-info/
