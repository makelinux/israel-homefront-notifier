# Israel Homefront Notifier - Linux

Linux-specific installation and usage guide.

## Prerequisites

- Linux with systemd
- Python 3.10+
- `notify-send` (usually included with desktop environments)
  - Debian/Ubuntu: `sudo apt install libnotify-bin`
  - Fedora/RHEL: `sudo dnf install libnotify`
  - Arch: `sudo pacman -S libnotify`
- Optional: `certifi` for reliable SSL certificate handling
  ```bash
  pip3 install certifi
  ```

## Quick start

```bash
git clone https://github.com/amito/israel-homefront-macos-notifier.git
cd israel-homefront-macos-notifier

# Edit the city list
vi config.json

# Install as a systemd user service
./install.sh
```

## Configuration

Edit `config.json`:

```json
{
  "cities": ["תל אביב - יפו", "חיפה"],
  "poll_interval_seconds": 5,
  "lang": "he"
}
```

## Service management

### Install

```bash
./install.sh
# or directly
./install-linux.sh
```

Creates systemd user service at `~/.config/systemd/user/oref-notifier.service`

### Check status

```bash
systemctl --user status oref-notifier
```

### View logs

```bash
# Follow logs
journalctl --user -u oref-notifier -f

# Last 50 lines
journalctl --user -u oref-notifier -n 50

# Logs since last boot
journalctl --user -u oref-notifier -b
```

### Start/stop manually

```bash
systemctl --user start oref-notifier
systemctl --user stop oref-notifier
systemctl --user restart oref-notifier
```

### Uninstall

```bash
./uninstall.sh
# or directly
./uninstall-linux.sh
```

This stops the service and removes the systemd unit file.
Seen-alerts data in `~/.oref-notifier/` is preserved.

To remove everything:
```bash
./uninstall.sh
rm -rf ~/.oref-notifier
```

## Troubleshooting

### Notifications not appearing

Check if notify-send works:
```bash
notify-send "Test" "This is a test notification"
```

Verify DISPLAY and DBUS_SESSION_BUS_ADDRESS are set:
```bash
systemctl --user show-environment | grep -E "DISPLAY|DBUS"
```

If missing, add to the service file:
```bash
systemctl --user edit oref-notifier
```

Add under `[Service]`:
```ini
Environment="DISPLAY=:0"
Environment="DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus"
```

### Service not starting

Check logs:
```bash
journalctl --user -u oref-notifier -n 100
```

Verify Python path:
```bash
which python3
```

Check config file exists:
```bash
cat config.json
```

### Service stops after logout

Enable lingering to keep user services running:
```bash
loginctl enable-linger $USER
```

## How it works

1. Polls the Pikud HaOref alerts history API every few seconds
2. Tracks seen alerts in `~/.oref-notifier/seen_alerts.json`
3. Sends desktop notifications via `notify-send -u critical`
4. On first run, seeds all existing alerts as "seen" to avoid notification flood
5. Runs as systemd user service with automatic restart on failure

## License

[MIT](LICENSE)
