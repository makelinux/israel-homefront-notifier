#!/usr/bin/env python3
"""Oref Notifier — Pikud HaOref alert monitor with macOS notifications."""

import json


def load_config(path: str) -> dict:
    """Load configuration from a JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
