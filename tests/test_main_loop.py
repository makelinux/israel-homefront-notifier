import unittest
from unittest.mock import patch, MagicMock, call


class TestProcessAlerts(unittest.TestCase):
    """Test the process_alerts function that checks for new alerts."""

    @patch("oref_notifier.send_notification")
    def test_new_alert_triggers_notification(self, mock_notify):
        from oref_notifier import process_alerts

        alerts = [
            {"rid": 100, "category": 1, "category_desc": "rockets",
             "NAME_HE": "test", "time": "10:00:00"},
        ]
        seen = set()
        new_seen = process_alerts(alerts, seen)
        mock_notify.assert_called_once_with(alerts[0])
        self.assertIn(100, new_seen)

    @patch("oref_notifier.send_notification")
    def test_already_seen_alert_skipped(self, mock_notify):
        from oref_notifier import process_alerts

        alerts = [
            {"rid": 100, "category": 1, "category_desc": "rockets",
             "NAME_HE": "test", "time": "10:00:00"},
        ]
        seen = {100}
        new_seen = process_alerts(alerts, seen)
        mock_notify.assert_not_called()
        self.assertIn(100, new_seen)

    @patch("oref_notifier.send_notification")
    def test_mixed_new_and_seen(self, mock_notify):
        from oref_notifier import process_alerts

        alerts = [
            {"rid": 100, "category": 1, "category_desc": "a",
             "NAME_HE": "x", "time": "10:00:00"},
            {"rid": 200, "category": 14, "category_desc": "b",
             "NAME_HE": "y", "time": "11:00:00"},
        ]
        seen = {100}
        new_seen = process_alerts(alerts, seen)
        mock_notify.assert_called_once_with(alerts[1])
        self.assertEqual(new_seen, {100, 200})


class TestSeedOnFirstRun(unittest.TestCase):
    """On first run, all current alerts are marked seen without notifying."""

    @patch("oref_notifier.send_notification")
    def test_seed_marks_all_seen_no_notify(self, mock_notify):
        from oref_notifier import seed_seen_alerts

        alerts = [
            {"rid": 1, "category": 1, "category_desc": "a",
             "NAME_HE": "x", "time": "10:00:00"},
            {"rid": 2, "category": 14, "category_desc": "b",
             "NAME_HE": "y", "time": "11:00:00"},
        ]
        seen = seed_seen_alerts(alerts)
        mock_notify.assert_not_called()
        self.assertEqual(seen, {1, 2})


if __name__ == "__main__":
    unittest.main()
