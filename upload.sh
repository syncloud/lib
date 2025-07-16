#!/bin/bash -e

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

export HOME=$DIR
set +x
if [ -z "$PYPI_LOGIN" ]; then
  echo "PYPI_LOGIN must be set"
  exit 1
fi
cat >$HOME/.pypirc <<EOF
[distutils]
index-servers = pypi

[pypi]
username: ${PYPI_LOGIN}
password: ${PYPI_PASSWORD}
EOF
set -x

pip install twine build
python -m build
twine upload dist/*
