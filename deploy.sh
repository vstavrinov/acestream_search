#!/bin/bash -e

REST="curl -siX POST                            \
    -H 'Accept: application/vnd.github.v3+json' \
    -H 'Authorization: token $TOKEN'            \
    -d '{\"ref\": \"master\",
         \"inputs\":
           {\"deploy\": \"true\"}
        }'                                      \
    https://api.github.com/repos/$ENDPOINT/dispatches"

RETURN="$(eval "$REST")"
echo "$RETURN"
STATUS=$(echo "$RETURN" |
    head -1            |
    awk '{print $2}')

if [ ${STATUS:=400} -ge 400 ]; then
    set -x -v
    eval "$REST"
    exit 1
fi
