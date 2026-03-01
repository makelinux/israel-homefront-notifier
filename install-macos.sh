#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PLIST_NAME="com.oref.notifier"
PLIST_PATH="$HOME/Library/LaunchAgents/${PLIST_NAME}.plist"
LOG_DIR="$HOME/Library/Logs/oref-notifier"

# Find python3
PYTHON="$(command -v python3 || true)"
[ "$PYTHON" ] || { echo "Error: python3 not found in PATH" >&2; exit 1; }

# Create required directories
mkdir -p "$LOG_DIR"
mkdir -p "$(dirname "$PLIST_PATH")"

# Write the plist
cat > "$PLIST_PATH" << PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>${PLIST_NAME}</string>
    <key>ProgramArguments</key>
    <array>
        <string>${PYTHON}</string>
        <string>${SCRIPT_DIR}/israel_homefront_notifier.py</string>
        <string>${SCRIPT_DIR}/config.json</string>
    </array>
    <key>WorkingDirectory</key>
    <string>${SCRIPT_DIR}</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>${LOG_DIR}/oref.log</string>
    <key>StandardErrorPath</key>
    <string>${LOG_DIR}/oref.log</string>
</dict>
</plist>
PLIST

# Load the service
launchctl unload "$PLIST_PATH" 2>/dev/null || true
launchctl load "$PLIST_PATH"

echo "Installed and started ${PLIST_NAME}"
echo "Logs: ${LOG_DIR}/oref.log"
echo "To stop: launchctl unload ${PLIST_PATH}"
