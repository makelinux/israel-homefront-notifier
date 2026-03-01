import json
import os
import tempfile
import unittest


class TestLoadConfig(unittest.TestCase):
    def test_loads_config_from_file(self):
        from israel_homefront_notifier import load_config

        config_data = {
            "cities": ["נתניה - מזרח"],
            "poll_interval_seconds": 5,
            "lang": "he",
        }
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            json.dump(config_data, f)
            f.flush()
            result = load_config(f.name)

        os.unlink(f.name)
        self.assertEqual(result["cities"], ["נתניה - מזרח"])
        self.assertEqual(result["poll_interval_seconds"], 5)
        self.assertEqual(result["lang"], "he")

    def test_config_missing_file_raises(self):
        from israel_homefront_notifier import load_config

        with self.assertRaises(FileNotFoundError):
            load_config("/nonexistent/config.json")


class TestReverseHebrew(unittest.TestCase):
    def test_reverses_hebrew_string(self):
        from israel_homefront_notifier import reverse_hebrew

        self.assertEqual(reverse_hebrew("חרזמ - הינתנ"), "נתניה - מזרח")

    def test_leaves_non_hebrew_unchanged(self):
        from israel_homefront_notifier import reverse_hebrew

        self.assertEqual(reverse_hebrew("Netanya - East"), "Netanya - East")

    def test_reverses_hebrew_without_dash(self):
        from israel_homefront_notifier import reverse_hebrew

        self.assertEqual(reverse_hebrew("ביבא לת"), "תל אביב")

    def test_empty_string(self):
        from israel_homefront_notifier import reverse_hebrew

        self.assertEqual(reverse_hebrew(""), "")


if __name__ == "__main__":
    unittest.main()
