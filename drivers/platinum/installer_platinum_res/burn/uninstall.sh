#!/bin/bash

echo                            # Initial newline, adds to style ;)
echo "Worker starts..."

test "$(whoami)" != 'root' \
    && echo "You need to be root to execute this script" \
    && exit 1

# Delete panel installation
echo "Deleting panel executable"
rm -rf /opt/platinum

# Delete desktop file and icons
echo "Deleting application registers"
rm -f /usr/share/applications/platinum.desktop
find /usr/share/icons -type f -name "platinum.png" -exec rm {} \;

# Update icon cache
echo "Updating icon cache"
[ -x $(which gtk-update-icon-cache) ] \
    && gtk-update-icon-cache /usr/share/icons/hicolor \
    && gtk-update-icon-cache /usr/share/icons/HighContrast

echo "Remove icon cache for KDE"
KDE_CACHE="/var/tmp/kdecache-$USER/icon-cache.kcache"
[ -e $KDE_CACHE ] && rm -f $KDE_CACHE

# Remove udev rule
RULE_FN="/etc/udev/rules.d/*-platinum.rules"
echo Removing $RULE_FN
rm -f $RULE_FN

exit 0
