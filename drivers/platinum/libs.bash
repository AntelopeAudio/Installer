#!/bin/bash
#
# Copy all linked libraries to ./libs or $1, if supplied.  List of
# libraries is acquired by examining local shared objects.
#

OUTDIR=$1
[ -z $OUTDIR ] && OUTDIR=./libs
mkdir -p $OUTDIR

# Filter by globing pattern
PATTERN=$2
[ -z $PATTERN ] && PATTERN=*

LIBS=$(
for SO in ./*.so
do
    ldd $SO | grep -Fe "=>" | grep -Po -e "(/[^/\s]+)+"
done | sort -u
)

for LIB in $LIBS
do
    if [[ $(basename $LIB) == $PATTERN ]]; then
        DEST=$OUTDIR/$(basename $LIB)
        echo "Copying $LIB to $DEST"
        cp $LIB $DEST
    fi
done
