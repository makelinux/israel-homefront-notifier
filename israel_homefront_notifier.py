#!/usr/bin/env python3
"""israel-homefront-notifier — Pikud HaOref alert monitor with native notifications."""

import json
import logging
import os
import ssl
import sys
import time
import unicodedata
from datetime import datetime
from urllib.parse import quote
from urllib.request import Request, urlopen

from notifier import send_notification

BASE_URL = "https://alerts-history.oref.org.il/Shared/Ajax/GetAlarmsHistory.aspx"
STATE_PATH = os.path.expanduser("~/.oref-notifier/state.yaml")

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


def load_state():
    """Load state from YAML file. Returns (last_rid, last_event)."""
    try:
        with open(STATE_PATH) as f:
            state = {}
            for line in f:
                if ':' in line:
                    k, v = line.split(':', 1)
                    state[k.strip()] = v.strip()
            return int(state.get('last_rid', 0)), float(state.get('last_event', 0))
    except (FileNotFoundError, ValueError):
        return 0, 0


def save_state(last_rid, last_event):
    """Save state to YAML file."""
    os.makedirs(os.path.dirname(STATE_PATH), exist_ok=True)
    with open(STATE_PATH, "w") as f:
        f.write(f"last_rid: {last_rid}\nlast_event: {last_event}\n")


def elapsed_str(last_event):
    """Format elapsed time since last event as HH:MM:SS."""
    e = int(time.time() - last_event)
    return f"{e // 3600:02d}:{e % 3600 // 60:02d}:{e % 60:02d}"


def last_event_from_alerts(alerts):
    """Derive last event time from most recent alert."""
    if not alerts:
        return time.time()
    latest = max(a["alertDate"] for a in alerts)
    return datetime.fromisoformat(latest.replace('T', ' ')).timestamp()


def process_alerts(alerts, last_rid, last_event):
    """Check for new alerts, send notifications. Returns (last_rid, last_event)."""
    for alert in alerts:
        rid = alert["rid"]
        if rid > last_rid:
            cat = alert['category']
            no_bold = cat in (5, 6, 13, 14) or 16 <= cat <= 28
            bold = "" if no_bold else "\033[1m"
            reset = "" if no_bold else "\033[0m"
            dt = datetime.fromisoformat(alert['alertDate'].replace('T', ' '))
            print(f"\r{bold}{dt.strftime('%y-%m-%d %H:%M:%S')} {cat} {alert['category_desc']}{reset}")
            t = dt.timestamp()
            if t > last_event:
                last_event = t
            if rid > last_rid:
                last_rid = rid
            send_notification(alert)
    save_state(last_rid, last_event)
    return last_rid, last_event


def main() -> None:
    """Main entry point -- polling loop."""
    config_path = sys.argv[1] if len(sys.argv) > 1 else "config.json"
    config = load_config(config_path)
    cities = config["cities"]
    lang = config.get("lang", "he")
    interval = config.get("poll_interval_seconds", 5)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )

    last_rid, last_event = load_state()

    alerts = fetch_alerts(cities, lang)
    if alerts:
        last_event = last_event_from_alerts(alerts)
        if not last_rid:
            last_rid = max(a["rid"] for a in alerts)
        save_state(last_rid, last_event)

    logger.info("Polling every %ds for cities: %s", interval, ", ".join(cities))

    last_poll = 0
    while True:
        now = time.monotonic()
        if now - last_poll >= interval:
            last_poll = now
            alerts = fetch_alerts(cities, lang)
            if alerts:
                last_rid, last_event = process_alerts(alerts, last_rid, last_event)
        print(f"\r{elapsed_str(last_event)}", end='', flush=True)
        time.sleep(1)


if __name__ == "__main__":
    main()
