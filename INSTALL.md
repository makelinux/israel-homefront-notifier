# Installation

## Prerequisites

- macOS 10.15 or later
- Python 3.10+
- (Optional) `certifi` for reliable SSL certificate handling:
  ```bash
  pip3 install certifi
  ```

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/amito/israel-homefront-macos-notifier.git
   cd israel-homefront-macos-notifier
   ```

2. Edit `config.json` with your cities:
   ```json
   {
     "cities": ["תל אביב - יפו"],
     "poll_interval_seconds": 5,
     "lang": "he"
   }
   ```

3. Test manually:
   ```bash
   python3 israel_homefront_notifier.py
   ```

## Install as a launchd service

The included `install.sh` script registers the notifier as a launchd user agent that starts automatically at login and restarts on failure.

```bash
./install.sh
```

This will:
- Create a LaunchAgent plist at `~/Library/LaunchAgents/com.oref.notifier.plist`
- Start the service immediately
- Write logs to `~/Library/Logs/oref-notifier/oref.log`

### Checking status

```bash
launchctl list | grep oref
```

### Viewing logs

```bash
tail -f ~/Library/Logs/oref-notifier/oref.log
```

## Uninstall

```bash
./uninstall.sh
```

This stops the service and removes the LaunchAgent plist. Your seen-alerts data in `~/.oref-notifier/` is preserved.

To remove everything:
```bash
./uninstall.sh
rm -rf ~/.oref-notifier
```
