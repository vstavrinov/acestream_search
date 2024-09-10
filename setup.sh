#!/bin/bash

docker run --name acestream-engine --detach --publish 6878:6878 \
    vstavrinov/acestream-engine
pip install --disable-pip-version-check --upgrade pip setuptools wheel
pip install pytest-cov codecov flake8

