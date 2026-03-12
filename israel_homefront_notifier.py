#!/usr/bin/env python3
"""israel-homefront-notifier — Pikud HaOref alert monitor with native notifications."""

import json
import logging
import os
import ssl
import sys
import time
import unicodedata
from urllib.parse import quote
from urllib.request import Request, urlopen

from notifier import send_notification

BASE_URL = "https://alerts-history.oref.org.il/Shared/Ajax/GetAlarmsHistory.aspx"
SEEN_ALERTS_PATH = os.path.expanduser("~/.oref-notifier/seen_alerts.json")

logger = logging.getLogger("israel_homefront_notifier")


def _is_hebrew(text: str) -> bool:
    """Check if text contains Hebrew characters."""
    return any(unicodedata.name(c, "").startswith("HEBREW") for c in text)


def load_config(path: str) -> dict:
    """Load configuration from a JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_url(cities: list[str], lang: str) -> str:
    """Build the Oref API URL with city query parameters."""
    params = f"lang={lang}&mode=0"
    for i, city in enumerate(cities):
        params += f"&city_{i}={quote(city)}"
    return f"{BASE_URL}?{params}"


def _ssl_context() -> ssl.SSLContext:
    """Create an SSL context, using certifi certs if available."""
    ctx = ssl.create_default_context()
    try:
        import certifi
        ctx.load_verify_locations(certifi.where())
    except ImportError:
        pass
    return ctx


def fetch_alerts(cities: list[str], lang: str) -> list[dict]:
    """Fetch alerts from the Oref API. Returns [] on error."""
    url = build_url(cities, lang)
    retries = 3
    for attempt in range(retries):
        try:
            #print(url)
            req = Request(url)
            req.add_header("Referer", "https://www.oref.org.il/")
            req.add_header("X-Requested-With", "XMLHttpRequest")
            with urlopen(req, timeout=10, context=_ssl_context()) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            if attempt < retries - 1:
                logger.debug("Fetch attempt %d/%d failed: %s, retrying in 2s",
                           attempt + 1, retries, type(e).__name__)
                time.sleep(2)
            else:
                logger.warning("Failed to fetch alerts after %d attempts: %s", retries, type(e).__name__)
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


def seed_seen_alerts(alerts: list[dict]) -> set[int]:
    """Mark all current alerts as seen without notifying (first-run behavior)."""
    return {a["rid"] for a in alerts}


def process_alerts(alerts: list[dict], seen: set[int]) -> set[int]:
    """Check for new alerts, send notifications, return updated seen set."""
    updated = set(seen)
    for alert in alerts:
        rid = alert["rid"]
        if rid not in seen:
            #print(alert)
            cat = alert['category']
            # Don't bold categories: 5, 6, 13, 14, 16-28
            no_bold = cat in (5, 6, 13, 14) or 16 <= cat <= 28
            bold = "" if no_bold else "\033[1m"
            reset = "" if no_bold else "\033[0m"
            print(f"{bold}{alert['time']} [{cat}] {alert['category_desc']}{reset}")
            send_notification(alert)
            updated.add(rid)
    return updated


def main() -> None:
    """Main entry point -- polling loop."""
    config_path = sys.argv[1] if len(sys.argv) > 1 else "config.json"
    config = load_config(config_path)
    cities = config["cities"]
    lang = config.get("lang", "he")
    interval = config.get("poll_interval_seconds", 5)
    seen_path = os.path.expanduser("~/.oref-notifier/seen_alerts.json")

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )

    seen = load_seen_alerts(seen_path)
    first_run = len(seen) == 0

    print(build_url(cities, lang))
    alerts = fetch_alerts(cities, lang)
    print(len(alerts))
    if first_run:
        logger.info("First run -- seeding seen alerts")
        alerts = fetch_alerts(cities, lang)
        seen = seed_seen_alerts(alerts)
        save_seen_alerts(seen_path, seen)
        logger.info("Seeded %d alerts", len(seen))

    logger.info("Polling every %ds for cities: %s", interval, ", ".join(cities))

    while True:
        alerts = fetch_alerts(cities, lang)
        if alerts:
            seen = process_alerts(alerts, seen)
            save_seen_alerts(seen_path, seen)
        time.sleep(interval)


if __name__ == "__main__":
    main()
