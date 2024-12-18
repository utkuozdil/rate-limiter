import json
import ipaddress

from src.core.config import DYNAMO_TABLE_NAME_IP_LIST
from src.core.ip_list_manager import IPListManager
from src.services.dynamo import DynamoHelper

dynamo_helper = DynamoHelper(DYNAMO_TABLE_NAME_IP_LIST)
ip_list_manager = IPListManager(dynamo_helper)


def is_valid_ip(ip: str) -> bool:
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def handler(event, _context):
    try:
        body = json.loads(event["body"])
        ip = body.get("ip")
        status = body.get("status")

        if not ip or not is_valid_ip(ip) or status not in ["whitelist", "blacklist"]:
            return {"statusCode": 400, "body": json.dumps(
                {"message": "Invalid request. Provide 'ip' and 'status' as 'whitelist' or 'blacklist'."})}

        ip_list_manager.update_ip_address_status(ip_address=ip, status=status)

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "IP address status has been updated"})
        }
    except Exception as e:
        print(f"Error handling request: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Internal server error"})
        }
