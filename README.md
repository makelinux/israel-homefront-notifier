# Israel Homefront Notifier

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org)

A cross-platform alert monitor for Israel's Home Front Command (Pikud HaOref).
Polls the official API and delivers native notifications for rocket alerts, safe-room updates, and other warnings in your configured cities.

Supports macOS and Linux.

**Linux users:** See [README-linux.md](README-linux.md) for Linux-specific installation and usage.

## Features

- Native notifications with sound
- Configurable city list (supports Hebrew names)
- Runs as a background service
- Lightweight -- pure Python, no external dependencies required (optional `certifi` for SSL)
- First-run seeding to avoid duplicate notifications on startup

## Quick start

```bash
git clone https://github.com/amito/israel-homefront-macos-notifier.git
cd israel-homefront-macos-notifier

# Edit the city list
vi config.json

# Install as a service (starts automatically)
./install.sh
```

See [INSTALL.md](INSTALL.md) for detailed instructions.

## Configuration

Edit `config.json`:

```json
{
  "cities": ["תל אביב - יפו", "חיפה"],
  "poll_interval_seconds": 5,
  "lang": "he"
}
```

| Field | Description | Default |
|-------|-------------|---------|
| `cities` | List of city names in Hebrew | *required* |
| `poll_interval_seconds` | Seconds between API polls | `5` |
| `lang` | API language code | `"he"` |

## How it works

1. Polls the Pikud HaOref alerts history API every few seconds
2. Tracks seen alerts in `~/.oref-notifier/seen_alerts.json`
3. Sends a native notification for each new alert
4. On first run, seeds all existing alerts as "seen" to avoid a notification flood

## Pushy demo

`pushy_demo.py` demonstrates push notifications using Pushy SDK (alternative to polling).

**Setup:**
1. Register at [pushy.me](https://dashboard.pushy.me/) to get an app ID
2. Install SDK: `pip install PushySDK`
3. Run: `./pushy_demo.py --app-id YOUR_APP_ID --topics test,alerts`

**Usage:**
```bash
./pushy_demo.py --app-id abc123 --topics test
```

Or configure in `pushy_config.json`:
```json
{
  "app_id": "YOUR_PUSHY_APP_ID",
  "topics": ["test", "alerts"]
}
```

Send test via [Pushy dashboard](https://dashboard.pushy.me/) to verify.

## License

[MIT](LICENSE)
