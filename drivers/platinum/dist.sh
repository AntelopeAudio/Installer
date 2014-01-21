#!/bin/bash

# We use the libs.bash script to copy some native libraries we depend on
LIBS_SCRIPT=$PWD/libs.bash

# Recreate the platinum dir
rm -rf platinum
mkdir platinum

# Run setup.py
python2 setup.py build

EXEDIR=./build/*
mv $EXEDIR platinum/files

# Create a symlink for easier launching
cd platinum
ln -s files/platinum platinum

# Now copy some native libraries to installer_platinum_res/libs
cd files
# $LIBS_SCRIPT ./installer_platinum_res/libs "*pyglib*"
# $LIBS_SCRIPT ./installer_platinum_res/libs "*libc.so.*"
# $LIBS_SCRIPT ./installer_platinum_res/libs "*libdl.so.*"
# $LIBS_SCRIPT ./installer_platinum_res/libs "*libm.so.*"
# $LIBS_SCRIPT ./installer_platinum_res/libs "*libpthread.so.*"
# $LIBS_SCRIPT ./installer_platinum_res/libs "*libutil.so.*"

# Go back and tar
cd ../..
tar cfz platinum.tar.gz platinum
