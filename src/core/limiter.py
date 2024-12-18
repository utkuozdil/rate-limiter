import time

from src.core.ip_list_manager import IPListManager
from src.services.dynamo import DynamoHelper


class RateLimiter:

    def __init__(self, dynamo_helper: DynamoHelper, ip_list_manager: IPListManager, threshold: int = 10,
                 window_seconds: int = 60):
        self.dynamo_helper = dynamo_helper
        self.ip_list_manager = ip_list_manager
        self.threshold = threshold
        self.window_seconds = window_seconds

    def is_request_allowed(self, identifier: str) -> bool:
        ip_status = self.ip_list_manager.get_ip_address_status(ip_address=identifier)
        if ip_status == "blacklist":
            print(f"IP {identifier} is blacklisted.")
            return False
        if ip_status == "whitelist":
            print(f"IP {identifier} is whitelisted.")
            return True
        return self._apply_rate_limit(identifier)

    def _apply_rate_limit(self, identifier: str) -> bool:
        current_time = int(time.time())
        item = self.dynamo_helper.get_rate_limit_data(identifier)

        if item:
            request_count = int(item["request_count"])
            time_window = int(item["time_window"])
            threshold = int(item["threshold"])
            window_seconds = int(item["window_seconds"])

            if current_time < time_window + self.window_seconds:
                if request_count >= self.threshold:
                    return False
                self.dynamo_helper.update_rate_limit_data(identifier, request_count + 1, time_window, threshold,
                                                          window_seconds)
            else:
                self.dynamo_helper.update_rate_limit_data(identifier, 1, current_time, threshold,
                                                          window_seconds)
        else:
            self.dynamo_helper.update_rate_limit_data(identifier, 1, current_time, self.threshold,
                                                      self.window_seconds)
        return True
