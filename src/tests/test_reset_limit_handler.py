import unittest
from unittest.mock import patch
import json

from src.handlers.reset_limit import handler


class TestHandler(unittest.TestCase):
    @patch("src.handlers.reset_limit.rate_limiter")
    def test_reset_limit(self, mock_rate_limiter):
        event = {
            "body": json.dumps({"ip": "192.168.1.2"})
        }

        response = handler(event, None)

        self.assertEqual(response["statusCode"], 200)
        self.assertEqual(
            json.loads(response["body"]),
            {"message": "Rate limit has been reset"}
        )

        mock_rate_limiter.reset_rate_limit.assert_called_once_with("192.168.1.2")