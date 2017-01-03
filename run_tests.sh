#!/usr/bin/env bash
# Runs the pytest tests
set -e

# Export as env variables
export PYTHONPATH='./'

# Install test requirements
pip install -r requirements.txt
pip install -r test-requirements.txt

# Run tests
py.test -v
