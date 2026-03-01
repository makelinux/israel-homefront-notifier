#!/bin/bash
set -euo pipefail

SERVICE_NAME="oref-notifier"
SERVICE_FILE="$HOME/.config/systemd/user/${SERVICE_NAME}.service"

if [ -f "$SERVICE_FILE" ]; then
    systemctl --user stop "${SERVICE_NAME}.service" 2>/dev/null || true
    systemctl --user disable "${SERVICE_NAME}.service" 2>/dev/null || true
    rm "$SERVICE_FILE"
    systemctl --user daemon-reload
    echo "Uninstalled ${SERVICE_NAME}.service"
else
    echo "Service not installed"
fi
