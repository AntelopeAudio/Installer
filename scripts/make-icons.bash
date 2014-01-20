#!/bin/bash

# This script, given an original image of size 384x384 or bigger,
# creates a set of icons suitable for a variety of desktop environments
# like Gnome, KDE and XFCE.  Depends on imagemagick.

# It creates the following structure:
# OUTDIR/HighContrast/16x16/apps/APP.png
# OUTDIR/HighContrast/22x22/apps/APP.png
# OUTDIR/HighContrast/32x32/apps/APP.png
# OUTDIR/HighContrast/48x48/apps/APP.png
# OUTDIR/HighContrast/256x256/apps/APP.png
# OUTDIR/hicolor/16x16/apps/APP.png
# OUTDIR/hicolor/22x22/apps/APP.png
# OUTDIR/hicolor/24x24/apps/APP.png
# OUTDIR/hicolor/32x32/apps/APP.png
# OUTDIR/hicolor/48x48/apps/APP.png
# OUTDIR/hicolor/64x64/apps/APP.png
# OUTDIR/hicolor/128x128/apps/APP.png
# OUTDIR/hicolor/192x192/apps/APP.png
# OUTDIR/hicolor/256x256/apps/APP.png
# OUTDIR/hicolor/384x384/apps/APP.png

# TODO y: HighContrast/scalable/apps-extra/APP-icon.svg

function usage {
    echo "Usage: $0 <image> [ -a <appname> | --appname <appname> ] " \
                           "[ -o <dir> | --outdir <dir> ]" >&2
    exit 1
}

# Get <image> argument
[ -z $1 ] && usage
IMAGE=$1
shift

# Get APPNAME and OUTDIR arguments
TEMP=$(getopt -o a:o: --long appname:,outdir: -- "$@")
[ $? != 0 ] && echo "Terminating..." >&2 && exit 1

eval set -- "$TEMP"

while true ; do
    case "$1" in
        -a|--appname) APPNAME=$2 ; shift 2 ;;
        -o|--outdir) OUTDIR=$2 ; shift 2 ;;
        --) shift  ; break ;;
        *) echo "Terminating... " >&2 ; exit 1 ;;
    esac
done

# Set default values for APPNAME and OUTDIR
[ -z $APPNAME ] && APPNAME=$(basename $IMAGE | sed "s/\.png//")
[ -z $OUTDIR ] && OUTDIR="."

# Actual converting: hicolor icons first
HICOLOR="16x16 22x22 24x24 32x32 48x48 64x64 128x128 192x192 256x256 384x384"
for SIZE in $HICOLOR; do
    DIR="$OUTDIR/hicolor/$SIZE/apps"
    mkdir -p $DIR
    OUTFILE="$DIR/$APPNAME.png"
    echo "Converting $OUTFILE"
    convert $IMAGE -resize $SIZE $OUTFILE
    [ $? != 0 ] && echo "Terminating..." >&2 && exit 1
done

# High contrast icons
HIGHCONTRAST="16x16 22x22 32x32 48x48 256x256"
for SIZE in $HIGHCONTRAST; do
    DIR="$OUTDIR/HighContrast/$SIZE/apps"
    mkdir -p $DIR
    OUTFILE="$DIR/$APPNAME.png"
    echo "Converting $OUTFILE"
    convert $IMAGE \
        -threshold 50% \
        -fx "(1.0/(1.0+exp(10.0*(0.5-u)))-0.006693)*1.0092503" \
        -resize $SIZE \
        $OUTFILE
    [ $? != 0 ] && echo "Terminating..." >&2 && exit 1
done

echo "Converting complete"
