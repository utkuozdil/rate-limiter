import json
import ipaddress

from src.core.config import DYNAMO_TABLE_NAME_IP_LIST, DYNAMO_TABLE_NAME, RATE_LIMIT_WINDOW_SECONDS, \
    RATE_LIMIT_THRESHOLD
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
        body = json.loads(event["body"])
        ip = body.get("ip")

        if not ip:
            return {"statusCode": 400, "body": json.dumps(
                {"message": "Invalid request. Provide 'ip' to reset rate limit"})}

        rate_limiter.reset_rate_limit(ip)

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Rate limit has been reset"})
        }
    except Exception as e:
        print(f"Error handling request: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Internal server error"})
        }
