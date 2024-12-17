import unittest
from unittest.mock import MagicMock
import time

from src.core.limiter import RateLimiter
from src.services.dynamo import DynamoHelper


class TestRateLimiter(unittest.TestCase):
    def setUp(self):
        self.mock_dynamo_helper = MagicMock(spec=DynamoHelper)
        self.rate_limiter = RateLimiter(self.mock_dynamo_helper, threshold=3, window_seconds=60)
        self.current_time = int(time.time())

    def test_new_user_first_request_allowed(self):
        self.mock_dynamo_helper.get_rate_limit_data.return_value = None

        result = self.rate_limiter.is_request_allowed("user123")

        self.assertTrue(result)
        self.mock_dynamo_helper.update_rate_limit_data.assert_called_once_with(
            "user123", 1, self.current_time
        )

    def test_request_within_rate_limit(self):
        self.mock_dynamo_helper.get_rate_limit_data.return_value = {
            "request_count": 2,
            "time_window": self.current_time,
        }

        result = self.rate_limiter.is_request_allowed("user123")

        self.assertTrue(result)
        self.mock_dynamo_helper.update_rate_limit_data.assert_called_once_with(
            "user123", 3, self.current_time
        )

    def test_request_exceeding_rate_limit(self):
        self.mock_dynamo_helper.get_rate_limit_data.return_value = {
            "request_count": 3,
            "time_window": self.current_time,
        }

        result = self.rate_limiter.is_request_allowed("user123")

        self.assertFalse(result)
        self.mock_dynamo_helper.update_rate_limit_data.assert_not_called()

    def test_request_after_time_window_reset(self):
        self.mock_dynamo_helper.get_rate_limit_data.return_value = {
            "request_count": 3,
            "time_window": self.current_time - 61,
        }

        result = self.rate_limiter.is_request_allowed("user123")

        self.assertTrue(result)
        self.mock_dynamo_helper.update_rate_limit_data.assert_called_once_with(
            "user123", 1, self.current_time
        )