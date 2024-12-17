import os
from dotenv import load_dotenv

load_dotenv()

RATE_LIMIT_THRESHOLD = int(os.getenv("RATE_LIMIT_THRESHOLD", 10))
RATE_LIMIT_WINDOW_SECONDS = int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", 60))
DYNAMO_TABLE_NAME = os.getenv("DYNAMO_TABLE_NAME", "RateLimitTable")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
