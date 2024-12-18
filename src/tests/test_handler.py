import unittest
from unittest.mock import patch
import json
from src.handlers.app import handler


class TestHandler(unittest.TestCase):
    @patch("src.handlers.app.rate_limiter")
    def test_request_allowed(self, mock_rate_limiter):
        mock_rate_limiter.is_request_allowed.return_value = True, None

        event = {
            "headers": {
                "X-Forwarded-For": "192.168.1.1"
            }
        }

        response = handler(event, None)

        self.assertEqual(response["statusCode"], 200)
        self.assertEqual(
            json.loads(response["body"]),
            {"message": "Request allowed."}
        )

        mock_rate_limiter.is_request_allowed.assert_called_once_with("192.168.1.1")

    @patch("src.handlers.app.rate_limiter")
    def test_request_denied(self, mock_rate_limiter):
        mock_rate_limiter.is_request_allowed.return_value = False, None

        event = {
            "headers": {
                "X-Forwarded-For": "192.168.1.1"
            }
        }

        response = handler(event, None)

        self.assertEqual(response["statusCode"], 429)
        self.assertEqual(
            json.loads(response["body"]),
            {"message": "Too Many Requests. Try again later."}
        )

        mock_rate_limiter.is_request_allowed.assert_called_once_with("192.168.1.1")

    @patch("src.handlers.app.rate_limiter")
    def test_internal_server_error(self, mock_rate_limiter):
        mock_rate_limiter.is_request_allowed.side_effect = Exception("Unexpected error")

        event = {
            "headers": {
                "X-Forwarded-For": "192.168.1.1"
            }
        }

        response = handler(event, None)

        self.assertEqual(response["statusCode"], 500)
        self.assertEqual(
            json.loads(response["body"]),
            {"message": "Internal server error"}
        )

        mock_rate_limiter.is_request_allowed.assert_called_once_with("192.168.1.1")
