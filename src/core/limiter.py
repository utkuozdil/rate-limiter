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

    def is_request_allowed(self, identifier: str):
        ip_status = self.ip_list_manager.get_ip_address_status(ip_address=identifier)
        if ip_status and ip_status.get("status") == "blacklist":
            return False, ip_status
        elif ip_status and ip_status.get("status") == "whitelist":
            return True, ip_status
        else:
            return self._apply_rate_limit(identifier)

    def _apply_rate_limit(self, identifier: str):
        current_time = int(time.time())
        item = self.dynamo_helper.get_rate_limit_data(identifier)

        if item:
            request_count = int(item["request_count"])
            time_window = int(item["time_window"])
            threshold = int(item["threshold"])
            window_seconds = int(item["window_seconds"])

            if current_time < time_window + self.window_seconds:
                if request_count >= self.threshold:
                    return False, None
                self.dynamo_helper.update_rate_limit_data(identifier, request_count + 1, time_window, threshold,
                                                          window_seconds)
            else:
                self.dynamo_helper.update_rate_limit_data(identifier, 1, current_time, threshold,
                                                          window_seconds)
        else:
            self.dynamo_helper.update_rate_limit_data(identifier, 1, current_time, self.threshold,
                                                      self.window_seconds)
        return True, None

    def reset_rate_limit(self, identifier: str):
        current_time = int(time.time())
        self.dynamo_helper.update_rate_limit_data(identifier, 0, current_time, self.threshold,
                                                  self.window_seconds)

    def update_limit_config(self, identifier: str, threshold: int, window_seconds: int):
        current_time = int(time.time())
        item = self.dynamo_helper.get_rate_limit_data(identifier)
        if item:
            request_count = int(item["request_count"])
        else:
            request_count = 0
        self.dynamo_helper.update_rate_limit_data(identifier, request_count, current_time, threshold, window_seconds)
