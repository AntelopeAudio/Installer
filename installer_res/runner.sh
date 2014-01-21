#!/bin/bash

# Simple bash script that does two things:
# 1. Tries to run ./worker.sh with sudo
# 2. Tries to run ./worker.sh with su
# Returns 0 on success, 1 on error

# WORKER=$PWD/$1
WORKER=$1
PASSWORD=$2
RUNWD=$PWD

echo "WORKER=$WORKER"

# Check if password is supplied or not
if [ -z $1 ] || [ -z $2 ]; then
    echo "Usage: $0 <password> <worker script>"
    exit 1
fi

# First, we try using sudo.  If this fails, we try su
echo "Trying sudo... "
echo "$PASSWORD" | sudo -S $WORKER
SUCCESS=$?
if [ $SUCCESS -eq "0" ]; then
    # Yey, success!
    sudo -k                     # Reset timestamp
    exit 0
else
    echo "failure"
    # sudo is unsuccessful, let's try with su
    echo "Trying su... "
    su -c "bash $WORKER" - root 2>/dev/null <<EOF
$PASSWORD
EOF
    SUCCESS=$?
    if [ $SUCCESS -eq "0" ]; then
        # Yey, success!
        exit 0
    else
        echo "failure"
        exit 1
    fi
fi
