import json

from src.core.config import DYNAMO_TABLE_NAME, RATE_LIMIT_THRESHOLD, RATE_LIMIT_WINDOW_SECONDS, \
    DYNAMO_TABLE_NAME_IP_LIST
from src.core.ip_list_manager import IPListManager
from src.core.limiter import RateLimiter
from src.services.dynamo import DynamoHelper

dynamo_helper = DynamoHelper(DYNAMO_TABLE_NAME)
dynamo_helper_for_ip_list = DynamoHelper(DYNAMO_TABLE_NAME_IP_LIST)
ip_list_manager = IPListManager(dynamo_helper_for_ip_list)
rate_limiter = RateLimiter(dynamo_helper, ip_list_manager=ip_list_manager, threshold=RATE_LIMIT_THRESHOLD,
                           window_seconds=RATE_LIMIT_WINDOW_SECONDS)


def handler(event, _context):
    try:
        headers = event.get("headers", {})
        ip_address = headers.get("X-Forwarded-For", "unknown").split(',')[0].strip()

        allowed, ip_status = rate_limiter.is_request_allowed(ip_address)

        if allowed:
            return {
                "statusCode": 200,
                "body": json.dumps({"message": "Request allowed."})
            }
        elif not allowed and ip_status is not None:
            return {
                "statusCode": 200,
                "body": json.dumps({"message": "IP address has been added to blacklist. Please contact with admin"})
            }
        else:
            return {
                "statusCode": 429,
                "body": json.dumps({"message": "Too Many Requests. Try again later."})
            }

    except Exception as e:
        print(f"Error handling request: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Internal server error"})
        }
