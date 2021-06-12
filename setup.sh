#!/bin/bash

sudo apt-get update
sudo apt-get install -y --no-install-recommends \
    python-apsw                                 \
    libxml2-dev                                 \
    libxslt1-dev                                \
    libpython2.7
mkdir /opt/acestream
cd /opt/acestream
ACE_VERSION="3.1.49_debian_9.9_x86_64"
curl -s http://acestream.org/downloads/linux/acestream_${ACE_VERSION}.tar.gz |
tar xzf -
./acestreamengine --client-console --log-file acestream.log 2>&1 &
sleep 2
if ! curl -s http://localhost:6878/server/api?method=get_api_access_token; then
    echo "Acestream failed! See log:"
    tail acestream.log
    echo "Giving up"
    exit 1
fi
cd -
pip install --disable-pip-version-check --upgrade pip setuptools wheel
pip install pytest-cov pytest-flake8 codecov

