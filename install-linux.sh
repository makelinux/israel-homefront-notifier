#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SERVICE_NAME="oref-notifier"
SYSTEMD_DIR="$HOME/.config/systemd/user"
SERVICE_FILE="${SYSTEMD_DIR}/${SERVICE_NAME}.service"

# Find python3
PYTHON="$(command -v python3 || true)"
[ "$PYTHON" ] || { echo "Error: python3 not found in PATH" >&2; exit 1; }

# Create systemd directory
mkdir -p "$SYSTEMD_DIR"

# Write the service file
cat > "$SERVICE_FILE" << SERVICE
[Unit]
Description=Israel Homefront Alert Notifier
After=network.target

[Service]
Type=simple
ExecStart=${PYTHON} ${SCRIPT_DIR}/israel_homefront_notifier.py ${SCRIPT_DIR}/config.json
WorkingDirectory=${SCRIPT_DIR}
Restart=always
RestartSec=10

[Install]
WantedBy=default.target
SERVICE

# Enable and start the service
systemctl --user daemon-reload
systemctl --user enable "${SERVICE_NAME}.service"
systemctl --user restart "${SERVICE_NAME}.service"

echo "Installed and started ${SERVICE_NAME}.service"
echo "Status: systemctl --user status ${SERVICE_NAME}"
echo "Logs: journalctl --user -u ${SERVICE_NAME} -f"
echo "To stop: systemctl --user stop ${SERVICE_NAME}"
