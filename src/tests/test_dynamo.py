import unittest
from unittest.mock import MagicMock, patch
from src.services.dynamo import DynamoHelper


class TestDynamoHelper(unittest.TestCase):
    def setUp(self):
        self.mock_dynamo = MagicMock()
        self.mock_table = MagicMock()

        patcher = patch("boto3.resource")
        self.addCleanup(patcher.stop)
        self.mock_boto_resource = patcher.start()
        self.mock_boto_resource.return_value.Table.return_value = self.mock_table

        self.dynamo_helper = DynamoHelper("RateLimitTable")

    def test_get_rate_limit_data_exists(self):
        self.mock_table.get_item.return_value = {
            "Item": {"identifier": "user123", "request_count": 5, "time_window": 1700000000}
        }

        result = self.dynamo_helper.get_rate_limit_data("user123")

        self.mock_table.get_item.assert_called_once_with(Key={"identifier": "user123"})
        self.assertEqual(result["request_count"], 5)
        self.assertEqual(result["time_window"], 1700000000)

    def test_get_rate_limit_data_not_found(self):
        self.mock_table.get_item.return_value = {}

        result = self.dynamo_helper.get_rate_limit_data("unknown_user")

        self.mock_table.get_item.assert_called_once_with(Key={"identifier": "unknown_user"})
        self.assertIsNone(result)

    def test_update_rate_limit_data(self):
        self.dynamo_helper.update_rate_limit_data("user123", 3, 1700000000)

        self.mock_table.put_item.assert_called_once_with(
            Item={"identifier": "user123", "request_count": 3, "time_window": 1700000000}
        )
