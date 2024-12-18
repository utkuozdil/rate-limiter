import unittest
from unittest.mock import MagicMock

from src.core.ip_list_manager import IPListManager
from src.services.dynamo import DynamoHelper


class TestIPManager(unittest.TestCase):
    def setUp(self):
        self.mock_dynamo_helper = MagicMock(spec=DynamoHelper)
        self.ip_list_manager = IPListManager(self.mock_dynamo_helper)

    def test_update_ip_status(self):
        self.ip_list_manager.update_ip_address_status(ip_address="192.168.1.2", status="blacklist")
        self.mock_dynamo_helper.update_ip_status.assert_called_once_with(ip_address='192.168.1.2', status='blacklist')

    def test_update_ip_status_whitelist(self):
        self.ip_list_manager.update_ip_address_status(ip_address="192.168.1.2", status="whitelist")
        self.mock_dynamo_helper.update_ip_status.assert_called_once_with(ip_address='192.168.1.2', status='whitelist')