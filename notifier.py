"""Platform-specific notification handlers."""

import logging
import platform
import subprocess

logger = logging.getLogger(__name__)

CATEGORY_TITLES = {
    1: "\U0001f6a8 ירי רקטות וטילים",
    13: "\u2139\ufe0f עדכון מרחב מוגן",
    14: "\u26a0\ufe0f התרעות צפויות",
}


def send_notification(alert: dict) -> None:
    """Send a native notification for an alert (macOS or Linux)."""
    category = alert.get("category")
    title = CATEGORY_TITLES.get(category, alert.get("category_desc", "התרעה"))
    city = alert.get("NAME_HE", "")
    time_str = alert.get("time", "")[:5]
    body = f"{city} \u2022 {time_str}"

    sys_name = platform.system()
    if sys_name == "Darwin":
        # macOS - use osascript
        title_esc = title.replace('"', '\\"')
        body_esc = body.replace('"', '\\"')
        script = (
            f'display notification "{body_esc}" '
            f'with title "{title_esc}" '
            f'sound name "default"'
        )
        subprocess.run(["osascript", "-e", script], check=False)
    elif sys_name == "Linux":
        # Linux - use notify-send
        subprocess.run(["notify-send", "-u", "critical", title, body], check=False)
    else:
        logger.warning("Notifications not supported on %s", sys_name)
