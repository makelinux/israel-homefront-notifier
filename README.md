# Israel Homefront MacOS Native Notifier

A macOS menu-bar-free alert monitor for Israel's Home Front Command (Pikud HaOref).
Polls the official API and delivers native macOS notifications for rocket alerts, safe-room updates, and other warnings in your configured cities.

## Features

- Native macOS notifications with sound
- Configurable city list (supports Hebrew names)
- Runs as a background launchd service
- Lightweight -- pure Python, no external dependencies required (optional `certifi` for SSL)
- First-run seeding to avoid duplicate notifications on startup

## Quick start

```bash
git clone https://github.com/amito/israel-homefront-macos-notifier.git
cd israel-homefront-macos-notifier

# Edit the city list
vi config.json

# Install as a launchd service (starts automatically)
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
3. Sends a macOS notification (via `osascript`) for each new alert
4. On first run, seeds all existing alerts as "seen" to avoid a notification flood

## License

[MIT](LICENSE)
