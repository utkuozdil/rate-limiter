import boto3
from botocore.exceptions import ClientError


class DynamoHelper:
    def __init__(self, table_name: str):
        self.dynamo = boto3.resource("dynamodb")
        self.table = self.dynamo.Table(table_name)

    def _handle_error(self, message):
        raise Exception(message)

    def get_rate_limit_data(self, identifier: str) -> dict:
        try:
            response = self.table.get_item(Key={"identifier": identifier})
            return response.get("Item", None)
        except ClientError as e:
            self._handle_error(f"Error retrieving data for '{identifier}': {e.response['Error']['Message']}")

    def update_rate_limit_data(self, identifier: str, request_count: int, time_window: int, threshold: int,
                               window_seconds: int):
        try:
            self.table.put_item(
                Item={
                    "identifier": identifier,
                    "request_count": request_count,
                    "time_window": time_window,
                    "threshold": threshold,
                    "window_seconds": window_seconds
                }
            )
        except ClientError as e:
            self._handle_error(f"Error updating data for '{identifier}': {e.response['Error']['Message']}")

    def update_ip_status(self, ip_address: str, status: str):
        try:
            self.table.put_item(Item={"ip": ip_address, "status": status})
        except ClientError as e:
            self._handle_error(f"Error updating ip status for '{ip_address}': {e.response['Error']['Message']}")

    def get_ip_status(self, ip_address: str) -> dict:
        try:
            response = self.table.get_item(Key={"ip": ip_address})
            return response.get("Item", None)
        except ClientError as e:
            self._handle_error(
                f"Error retrieving ip address status for '{ip_address}': {e.response['Error']['Message']}")