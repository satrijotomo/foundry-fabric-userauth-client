import os
from dotenv import load_dotenv

load_dotenv()

TENANT_ID = os.getenv("TENANT_ID")

FOUNDRY_RESPONSES_URL = os.getenv("FOUNDRY_RESPONSES_URL")
FOUNDRY_ACTIVITY_URL = os.getenv("FOUNDRY_ACTIVITY_URL")
FABRIC_DATA_AGENT_URL = os.getenv("FABRIC_DATA_AGENT_URL")


def validate_config():
    missing = []
    if not TENANT_ID:
        missing.append("TENANT_ID")
    if not FOUNDRY_RESPONSES_URL:
        missing.append("FOUNDRY_RESPONSES_URL")
    if not FOUNDRY_ACTIVITY_URL:
        missing.append("FOUNDRY_ACTIVITY_URL")

    if missing:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing)}"
        )