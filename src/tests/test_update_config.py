import unittest
from unittest.mock import patch
import json

from src.handlers.update_config import handler


class TestHandler(unittest.TestCase):
    @patch("src.handlers.update_config.rate_limiter")
    def test_reset_limit(self, mock_rate_limiter):
        event = {
            "body": json.dumps({"ip": "192.168.1.2", "threshold": 20, "time_window": 120})
        }

        response = handler(event, None)

        self.assertEqual(response["statusCode"], 200)
        self.assertEqual(
            json.loads(response["body"]),
            {"message": "Rate limit configuration has been updated"}
        )

        mock_rate_limiter.update_limit_config.assert_called_once_with("192.168.1.2", 20, 120)