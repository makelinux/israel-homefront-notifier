import json
import os
import tempfile
import unittest


class TestSeenAlerts(unittest.TestCase):
    def test_load_returns_empty_set_if_file_missing(self):
        from oref_notifier import load_seen_alerts

        result = load_seen_alerts("/nonexistent/seen.json")
        self.assertEqual(result, set())

    def test_save_and_load_roundtrip(self):
        from oref_notifier import load_seen_alerts, save_seen_alerts

        with tempfile.NamedTemporaryFile(
            suffix=".json", delete=False
        ) as f:
            path = f.name

        try:
            save_seen_alerts(path, {100, 200, 300})
            loaded = load_seen_alerts(path)
            self.assertEqual(loaded, {100, 200, 300})
        finally:
            os.unlink(path)

    def test_save_creates_parent_directory(self):
        from oref_notifier import save_seen_alerts

        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "subdir", "seen.json")
            save_seen_alerts(path, {1, 2, 3})
            self.assertTrue(os.path.exists(path))


if __name__ == "__main__":
    unittest.main()
