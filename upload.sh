#!/bin/bash -e

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

export HOME=$DIR
set +x
cat >$HOME/.pypirc <<EOF
[distutils]
index-servers = pypi

[pypi]
username: $PYPI_LOGIN
password: $PYPI_PASSWORD
EOF
set -x

python setup.py sdist upload
    