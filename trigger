#!/usr/bin/env bash

BODY='{
    "request": {
        "branch":"master"
    }
}'

curl -s -X POST                             \
    -H "Content-Type: application/json"     \
    -H "Accept: application/json"           \
    -H "Travis-API-Version: 3"              \
    -H "Authorization: token $TRAVIS_TOKEN" \
    -d "$BODY"                              \
https://api.travis-ci.org/repo/$TRIGGER_REPO/requests

