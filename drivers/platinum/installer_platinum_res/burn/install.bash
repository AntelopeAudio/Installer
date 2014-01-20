#!/bin/bash

#
# Install control panel
#
echo                            # Initial newline, adds to style ;)
echo "Worker starts..."

test "$(whoami)" != 'root' \
    && echo "You need to be root to execute this script" \
    && exit 1

BASE_DIR=$(dirname ${BASH_SOURCE[0]})
DIST_DIR="$BASE_DIR/dist"
PLATINUM_DIR="$DIST_DIR/platinum"
USR_DIR="$DIST_DIR/usr"

cp -r $PLATINUM_DIR /opt
cp -r $USR_DIR /

# Update icon cache
echo "Updating icon cache for Gnome..."
[ -x $(which gtk-update-icon-cache) ] \
    && gtk-update-icon-cache /usr/share/icons/hicolor \
    && gtk-update-icon-cache /usr/share/icons/HighContrast

echo "Remove icon cache for KDE..."
KDE_CACHE="/var/tmp/kdecache-$USER/icon-cache.kcache"
[ -e $KDE_CACHE ] && rm -f $KDE_CACHE

#
# Make a new udev rule for this device
#
ID_VENDOR="23e5"
ID_PRODUCT="a013"

GRS=$(groups)
GRA=($GRS)
GR=${GRA[0]}
RULE="SUBSYSTEM==\"usb\", \
ATTRS{idVendor}==\"$ID_VENDOR\", \
ATTRS{idProduct}==\"$ID_PRODUCT\", \
GROUP=\"$GR\", \
MODE=\"0666\""

N=55
while true; do
    PATTERN="/etc/udev/rules.d/$N-*.rules"
    if [ -e $PATTERN ]; then
        let "N += 1"
    else
        RULE_FN="/etc/udev/rules.d/$N-platinum.rules"
        echo "echo $RULE >> $RULE_FN"
        echo "$RULE" >> "$RULE_FN"
        if [ $? == 0 ]; then
            echo "[udev] Success! File $RULE_FN successfully created"
        else
            echo "[udev] Failure! Please send us the output of this command"
            echo
            echo "[udev] DEBUG INFORMATION:"
            echo "[udev] \$USER=$USER"
            echo "[udev] \$GRS=$GRS"
            echo "[udev] \$GR=$GR"
        fi
        break
    fi
done

# Adding the rule to udev shouldn't affect the exit code
exit 0
