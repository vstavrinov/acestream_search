#!/bin/bash

CMD='
apk add nginx;
echo "
server {
    listen       80;
    location / {
        proxy_pass http://localhost:6878;
    }
}
" > /etc/nginx/http.d/default.conf;
nginx;
./acestreamengine --client-console;
'

docker run --detach --name acestream-engine --publish 6878:80 --env HOME=. \
    vstavrinov/acestream-engine sh -c "$CMD"

pip install --disable-pip-version-check --upgrade pip setuptools wheel
pip install pytest-cov codecov

