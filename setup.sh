#!/bin/bash

sudo apt-get update
sudo apt-get install -y --no-install-recommends \
    python-apsw                                 \
    libxml2-dev                                 \
    libxml2                                     \
    python3-lxml                                \
    python-libxml2                              \
    libxslt1-dev                                \
    libpython2.7                                \
    python-pkg-resources
mkdir /opt/acestream
cd /opt/acestream
ACE_VERSION="3.1.49_debian_9.9_x86_64"
curl -s http://acestream.org/downloads/linux/acestream_${ACE_VERSION}.tar.gz |
tar xzf -
./acestreamengine --client-console --log-file acestream.log 2>&1 &
cd -
pip install --disable-pip-version-check --upgrade pip setuptools wheel
pip install pytest-cov pytest-flake8 codecov

