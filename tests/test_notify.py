import platform
import unittest
from unittest.mock import patch, call


CATEGORY_TITLES = {
    1: "\U0001f6a8 ירי רקטות וטילים",
    13: "\u2139\ufe0f עדכון מרחב מוגן",
    14: "\u26a0\ufe0f התרעות צפויות",
}


class TestNotify(unittest.TestCase):
    @patch("notifier.subprocess.run")
    def test_sends_osascript_notification(self, mock_run):
        from notifier import send_notification

        alert = {
            "category": 1,
            "category_desc": "ירי רקטות וטילים",
            "NAME_HE": "נתניה - מזרח",
            "time": "18:45:19",
        }
        send_notification(alert)

        mock_run.assert_called_once()
        cmd = mock_run.call_args[0][0]

        sys_name = platform.system()
        if sys_name == "Darwin":
            self.assertEqual(cmd[0], "osascript")
            self.assertEqual(cmd[1], "-e")
            script = cmd[2]
            self.assertIn("נתניה - מזרח", script)
            self.assertIn("18:45", script)
        elif sys_name == "Linux":
            self.assertEqual(cmd[0], "notify-send")
            full = " ".join(cmd)
            self.assertIn("נתניה - מזרח", full)
            self.assertIn("18:45", full)

    @patch("notifier.subprocess.run")
    def test_uses_category_title(self, mock_run):
        from notifier import send_notification

        alert = {
            "category": 14,
            "category_desc": "בדקות הקרובות צפויות להתקבל התרעות באזורך",
            "NAME_HE": "תל אביב",
            "time": "10:30:00",
        }
        send_notification(alert)
        cmd = mock_run.call_args[0][0]

        sys_name = platform.system()
        if sys_name == "Darwin":
            script = cmd[2]
            self.assertIn("התרעות צפויות", script)
        elif sys_name == "Linux":
            self.assertIn("התרעות צפויות", " ".join(cmd))

    @patch("notifier.subprocess.run")
    def test_unknown_category_uses_desc(self, mock_run):
        from notifier import send_notification

        alert = {
            "category": 99,
            "category_desc": "סוג חדש",
            "NAME_HE": "חיפה",
            "time": "12:00:00",
        }
        send_notification(alert)
        cmd = mock_run.call_args[0][0]

        sys_name = platform.system()
        if sys_name == "Darwin":
            script = cmd[2]
            self.assertIn("סוג חדש", script)
        elif sys_name == "Linux":
            self.assertIn("סוג חדש", " ".join(cmd))


if __name__ == "__main__":
    unittest.main()
