from app.config import (
    TENANT_ID,
    FOUNDRY_RESPONSES_URL,
    FOUNDRY_ACTIVITY_URL,
    validate_config,
)
from app.auth import UserAuth
from app.foundry_client import FoundryAgentClient
import re


def extract_final_answer(response_json):
    """
    Extract ONLY the final assistant message text from Foundry response
    """
    for item in response_json.get("output", []):
        if (
            item.get("type") == "message"
            and item.get("role") == "assistant"
            and item.get("phase") == "final_answer"
        ):
            for content in item.get("content", []):
                if content.get("type") == "output_text":
                    return content.get("text")

    return "No final answer found."


def clean_text(text):
    """
    Remove citation markers like 【5:0†source】
    """
    return re.sub(r'【.*?】', '', text).strip()


def main():
    validate_config()

    auth = UserAuth(TENANT_ID)

    foundry = FoundryAgentClient(
        auth_provider=auth,
        responses_url=FOUNDRY_RESPONSES_URL,
        activity_url=FOUNDRY_ACTIVITY_URL
    )

    print("Signing in...")

    response = foundry.call_responses(
        "Return the number of rows in the dataset."
    )

    final_text = extract_final_answer(response)

    print("\n=== Foundry Agent Response ===\n")
    print(clean_text(final_text))


if __name__ == "__main__":
    main()