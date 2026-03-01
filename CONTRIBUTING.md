# Contributing

Contributions are welcome! Here's how to get started.

## Setup

```bash
git clone https://github.com/amito/israel-homefront-macos-notifier.git
cd israel-homefront-macos-notifier
```

Python 3.10+ is required. No external dependencies are needed for the core notifier (optional `certifi` for SSL).

## Running tests

```bash
uv run pytest -q
```

## Submitting changes

1. Fork the repository
2. Create a feature branch (`git checkout -b my-feature`)
3. Make your changes and add tests
4. Run the test suite to make sure everything passes
5. Commit with a clear message and open a pull request

## Guidelines

- Keep changes focused — one feature or fix per PR
- Add tests for new functionality
- Follow the existing code style (pure stdlib, no heavy dependencies)
- Use type hints on public functions

## Reporting issues

Open an issue on GitHub with:
- What you expected to happen
- What actually happened
- Steps to reproduce
- Your macOS and Python versions
