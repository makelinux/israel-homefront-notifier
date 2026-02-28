#!/usr/bin/env python3
"""Oref Notifier — Pikud HaOref alert monitor with macOS notifications."""

import json
import logging
import os
import subprocess
from urllib.parse import quote
from urllib.request import Request, urlopen

BASE_URL = "https://alerts-history.oref.org.il//Shared/Ajax/GetAlarmsHistory.aspx"
SEEN_ALERTS_PATH = os.path.expanduser("~/.oref-notifier/seen_alerts.json")

logger = logging.getLogger("oref_notifier")


def load_config(path: str) -> dict:
    """Load configuration from a JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_url(cities: list[str], lang: str) -> str:
    """Build the Oref API URL with city query parameters."""
    params = f"lang={lang}&mode=1"
    for i, city in enumerate(cities):
        params += f"&city_{i}={quote(city)}"
    return f"{BASE_URL}?{params}"


def fetch_alerts(cities: list[str], lang: str) -> list[dict]:
    """Fetch alerts from the Oref API. Returns [] on error."""
    url = build_url(cities, lang)
    try:
        req = Request(url)
        req.add_header("Referer", "https://www.oref.org.il/")
        req.add_header("X-Requested-With", "XMLHttpRequest")
        with urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception:
        logger.warning("Failed to fetch alerts", exc_info=True)
        return []


def load_seen_alerts(path: str) -> set[int]:
    """Load seen alert IDs from disk. Returns empty set if file missing."""
    try:
        with open(path, "r") as f:
            return set(json.load(f))
    except (FileNotFoundError, json.JSONDecodeError):
        return set()


def save_seen_alerts(path: str, seen: set[int]) -> None:
    """Save seen alert IDs to disk."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(sorted(seen), f)


CATEGORY_TITLES = {
    1: "\U0001f6a8 ירי רקטות וטילים",
    13: "\u2139\ufe0f עדכון מרחב מוגן",
    14: "\u26a0\ufe0f התרעות צפויות",
}


def send_notification(alert: dict) -> None:
    """Send a macOS notification for an alert via osascript."""
    category = alert.get("category")
    title = CATEGORY_TITLES.get(category, alert.get("category_desc", "התרעה"))
    city = alert.get("NAME_HE", "")
    time_str = alert.get("time", "")[:5]
    body = f"{city} \u2022 {time_str}"

    # Escape double quotes for AppleScript string literals
    title_esc = title.replace('"', '\\"')
    body_esc = body.replace('"', '\\"')

    script = (
        f'display notification "{body_esc}" '
        f'with title "{title_esc}" '
        f'sound name "default"'
    )
    subprocess.run(["osascript", "-e", script], check=False)
