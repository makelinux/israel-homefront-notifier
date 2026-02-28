#!/usr/bin/env python3
"""Oref Notifier — Pikud HaOref alert monitor with macOS notifications."""

import json
import logging
from urllib.parse import quote
from urllib.request import Request, urlopen

BASE_URL = "https://alerts-history.oref.org.il//Shared/Ajax/GetAlarmsHistory.aspx"

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
