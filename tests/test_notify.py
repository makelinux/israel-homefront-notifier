import unittest
from unittest.mock import patch, call


CATEGORY_TITLES = {
    1: "\U0001f6a8 ירי רקטות וטילים",
    13: "\u2139\ufe0f עדכון מרחב מוגן",
    14: "\u26a0\ufe0f התרעות צפויות",
}


class TestNotify(unittest.TestCase):
    @patch("israel_homefront_notifier.subprocess.run")
    def test_sends_osascript_notification(self, mock_run):
        from israel_homefront_notifier import send_notification

        alert = {
            "category": 1,
            "category_desc": "ירי רקטות וטילים",
            "NAME_HE": "נתניה - מזרח",
            "time": "18:45:19",
        }
        send_notification(alert)

        mock_run.assert_called_once()
        cmd = mock_run.call_args[0][0]
        self.assertEqual(cmd[0], "osascript")
        self.assertEqual(cmd[1], "-e")
        # The AppleScript should contain the notification text
        script = cmd[2]
        self.assertIn("נתניה - מזרח", script)
        self.assertIn("18:45", script)

    @patch("israel_homefront_notifier.subprocess.run")
    def test_uses_category_title(self, mock_run):
        from israel_homefront_notifier import send_notification

        alert = {
            "category": 14,
            "category_desc": "בדקות הקרובות צפויות להתקבל התרעות באזורך",
            "NAME_HE": "תל אביב",
            "time": "10:30:00",
        }
        send_notification(alert)
        script = mock_run.call_args[0][0][2]
        self.assertIn("התרעות צפויות", script)

    @patch("israel_homefront_notifier.subprocess.run")
    def test_unknown_category_uses_desc(self, mock_run):
        from israel_homefront_notifier import send_notification

        alert = {
            "category": 99,
            "category_desc": "סוג חדש",
            "NAME_HE": "חיפה",
            "time": "12:00:00",
        }
        send_notification(alert)
        script = mock_run.call_args[0][0][2]
        self.assertIn("סוג חדש", script)


if __name__ == "__main__":
    unittest.main()
