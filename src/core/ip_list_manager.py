
from src.services.dynamo import DynamoHelper


class IPListManager:

    def __init__(self, dynamo_helper: DynamoHelper):
        self.dynamo_helper = dynamo_helper

    def update_ip_address_status(self, ip_address: str, status: str):
        self.dynamo_helper.update_ip_status(ip_address=ip_address, status=status)

    def get_ip_address_status(self, ip_address: str) -> dict:
        return self.dynamo_helper.get_ip_status(ip_address=ip_address)