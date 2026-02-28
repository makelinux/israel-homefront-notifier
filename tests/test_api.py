import json
import unittest
from unittest.mock import patch, MagicMock


class TestBuildUrl(unittest.TestCase):
    def test_single_city(self):
        from oref_notifier import build_url

        url = build_url(["נתניה - מזרח"], "he")
        self.assertIn("lang=he", url)
        self.assertIn("mode=1", url)
        self.assertIn("city_0=", url)

    def test_multiple_cities(self):
        from oref_notifier import build_url

        url = build_url(["נתניה - מזרח", "תל אביב"], "he")
        self.assertIn("city_0=", url)
        self.assertIn("city_1=", url)


class TestFetchAlerts(unittest.TestCase):
    @patch("oref_notifier.urlopen")
    def test_parses_json_response(self, mock_urlopen):
        from oref_notifier import fetch_alerts

        alerts_data = [
            {
                "rid": 12345,
                "category": 1,
                "category_desc": "ירי רקטות וטילים",
                "alertDate": "2026-02-28T18:45:00",
                "NAME_HE": "נתניה - מזרח",
                "data": "נתניה - מזרח",
                "time": "18:45:19",
            }
        ]
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(alerts_data).encode("utf-8")
        mock_response.__enter__ = lambda s: s
        mock_response.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_response

        result = fetch_alerts(["נתניה - מזרח"], "he")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["rid"], 12345)

    @patch("oref_notifier.urlopen")
    def test_returns_empty_on_network_error(self, mock_urlopen):
        from oref_notifier import fetch_alerts

        mock_urlopen.side_effect = OSError("Connection refused")

        result = fetch_alerts(["נתניה - מזרח"], "he")
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
