#!/bin/bash

docker run --detach --name acestream-engine --publish 6878:6878 --env HOME=. \
    vstavrinov/acestream-engine ./acestreamengine --client-console

pip install --disable-pip-version-check --upgrade pip setuptools wheel
pip install pytest-cov pytest-flake8 codecov

