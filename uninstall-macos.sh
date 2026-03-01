#!/bin/bash
set -euo pipefail

PLIST_NAME="com.oref.notifier"
PLIST_PATH="$HOME/Library/LaunchAgents/${PLIST_NAME}.plist"

if [ -f "$PLIST_PATH" ]; then
    launchctl unload "$PLIST_PATH" 2>/dev/null || true
    rm "$PLIST_PATH"
    echo "Uninstalled ${PLIST_NAME}"
else
    echo "Service not installed"
fi
