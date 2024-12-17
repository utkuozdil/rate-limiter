import time

from src.services.dynamo import DynamoHelper


class RateLimiter:

    def __init__(self, dynamo_helper: DynamoHelper, threshold: int = 10, window_seconds: int = 60):
        self.dynamo_helper = dynamo_helper
        self.threshold = threshold
        self.window_seconds = window_seconds

    def is_request_allowed(self, identifier: str) -> bool:
        current_time = int(time.time())
        item = self.dynamo_helper.get_rate_limit_data(identifier)

        if item:
            request_count = int(item["request_count"])
            time_window = int(item["time_window"])

            if current_time < time_window + self.window_seconds:
                if request_count >= self.threshold:
                    return False
                self.dynamo_helper.update_rate_limit_data(identifier, request_count + 1, time_window)
            else:
                self.dynamo_helper.update_rate_limit_data(identifier, 1, current_time)
        else:
            self.dynamo_helper.update_rate_limit_data(identifier, 1, current_time)
        return True
