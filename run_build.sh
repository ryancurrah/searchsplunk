#!/usr/bin/env bash
# Creates a pip package and uploads to PyPi
set -e

pip install -U pip setuptools twine

echo "PyPi username: "
read PYPI_USERNAME

echo "PyPi password: "
read -s PYPI_PASSWORD

cat > ~/.pypirc << EOF
[distutils]
index-servers =
  pypi

[pypi]
username=${PYPI_USERNAME}
password=${PYPI_PASSWORD}
EOF

chmod 600 ~/.pypirc

# Build new package
python setup.py sdist

# Upload new package
twine upload dist/*

rm -f ~/.pypirc
