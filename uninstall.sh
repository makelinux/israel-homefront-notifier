#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

case "$(uname -s)" in
    Darwin)
        exec "$SCRIPT_DIR/uninstall-macos.sh"
        ;;
    Linux)
        exec "$SCRIPT_DIR/uninstall-linux.sh"
        ;;
    *)
        echo "Unsupported platform: $(uname -s)" >&2
        exit 1
        ;;
esac
