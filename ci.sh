#!/bin/sh

CI=$(basename $0)
VERSION=0.0
DESCRIPTION="Continuous integration"

[ -r ${CI%.*}.conf ] && . ./${CI%.*}.conf

usage ()
{
    echo -e "
    $DESCRIPTION

    Usage:

    $SELF_NAME [-LvdVh] [ -c CONF ] [-r REPO] [-i IMAGE] [ -b BUILD ]

    -c CONF
         Configuration file. If present, should be first option.

    -i IMAGE 
         Docker image, repeat the option for multiple images.

    -b BUILD
         Build script (commands) to run in the docker container

    -o  OPTIONS
         Docker extra options

    -r REPO
         Repository path [$REPO]
    -v
	    Verbose
    -d 
	    Debug
    -V
	    Version
    -h
	    Help
    "
    exit
}

OPTERR=0
while getopts c:i:r:o:vdVh OPTION; do
    case $OPTION in
	c)
	    CONF=$OPTARG
         [ -r $CONF ] && . $CONF
	    ;;
	r)
	    REPO=$OPTARG
	    ;;
	i)
         unset MATRIX
         MATRIX[0]=$OPTARG
	    ;;
	b)
	    BUILD="$OPTARG"
	    ;;
	o)
	    OPTIONS=$OPTARG
	    ;;
	v)
	    VERBOSE=" "
	    ;;
	d)
         DEBUG=true
	    ;;
	V)
	    echo -e "
        $SELF_NAME $VERSION ${VERBOSE:+\\n\\t$DESCRIPTION\\n}\\n}
	    "
	    exit
	    ;;
	h|*)
	    usage
	    ;;
    esac
done
shift  $[$OPTIND - 1]

: ${REPO:=$(pwd)}
: ${MATRIX:="busybox"}
: ${BUILD:="hostname"}

PROJECT=$(basename $REPO)
for IMAGE in ${MATRIX[@]}; do
    {
        RELEASE=${IMAGE#*:}
        LOG=${PROJECT}_${RELEASE}_$(date +%Y-%m-%d_%H-%M-%S).log
        SECONDS=0
        exec >> $LOG 2>&1 < /dev/null
        time echo "$BUILD" |
        docker run --rm -i -w /srv/$PROJECT -v ${REPO}:/srv/$PROJECT $OPTIONS $IMAGE sh ${DEBUG+-x -v} |
        while read LINE; do
            echo $(date "+%Y-%m-%d %H:%M:%S %z") $SECONDS $LINE 
        done
    } &
done
wait
