import boto3
from botocore.exceptions import ClientError


class DynamoHelper:
    def __init__(self, table_name: str):
        self.dynamo = boto3.resource("dynamodb")
        self.table = self.dynamo.Table(table_name)

    def get_rate_limit_data(self, identifier: str) -> dict:
        try:
            response = self.table.get_item(Key={"identifier": identifier})
            return response.get("Item", None)
        except ClientError as e:
            error_message = f"Error retrieving data for '{identifier}': {e.response['Error']['Message']}"
            print(error_message)
            raise Exception(error_message)

    def update_rate_limit_data(self, identifier: str, request_count: int, time_window: int):
        try:
            self.table.put_item(
                Item={
                    "identifier": identifier,
                    "request_count": request_count,
                    "time_window": time_window
                }
            )
        except ClientError as e:
            error_message = f"Error updating data for '{identifier}': {e.response['Error']['Message']}"
            print(error_message)
            raise Exception(error_message)
