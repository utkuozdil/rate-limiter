import unittest
from unittest.mock import patch
import json

from src.handlers.manage_ip_status import handler


class TestHandler(unittest.TestCase):
    @patch("src.handlers.manage_ip_status.ip_list_manager")
    def test_update_ip_status(self, mock_ip_list_manager):
        event = {
            "body": json.dumps({"ip": "192.168.1.2", "status": "blacklist"})
        }

        response = handler(event, None)

        self.assertEqual(response["statusCode"], 200)
        self.assertEqual(
            json.loads(response["body"]),
            {"message": "IP address status has been updated"}
        )

        mock_ip_list_manager.update_ip_address_status.assert_called_once_with(ip_address="192.168.1.2", status="blacklist")

    @patch("src.handlers.manage_ip_status.ip_list_manager")
    def test_internal_server_error(self, mock_ip_list_manager):
        mock_ip_list_manager.update_ip_address_status.side_effect = Exception("Unexpected error")

        event = {
            "body": json.dumps({"ip": "192.168.1.2", "status": "blacklist"})
        }

        response = handler(event, None)

        self.assertEqual(response["statusCode"], 500)
        self.assertEqual(
            json.loads(response["body"]),
            {"message": "Internal server error"}
        )

        mock_ip_list_manager.update_ip_address_status.assert_called_once_with(ip_address="192.168.1.2", status="blacklist")

    @patch("src.handlers.manage_ip_status.ip_list_manager")
    def test_wrong_input(self, mock_ip_list_manager):
        event = {
            "body": json.dumps({"ip": "192.168.1.2", "status": "blacklist1"})
        }

        response = handler(event, None)

        self.assertEqual(response["statusCode"], 400)
        self.assertEqual(
            json.loads(response["body"]),
            {"message": "Invalid request. Provide 'ip' and 'status' as 'whitelist' or 'blacklist'."}
        )