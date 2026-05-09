import requests
from typing import Any, Dict


class FabricDataAgentDirectClient:
    """
    Direct user-authenticated Fabric Data Agent client.

    This follows the documented external-app pattern where the user signs in
    interactively and the data agent runs with the user's permissions.
    """

    def __init__(self, auth_provider, data_agent_url: str):
        if not data_agent_url:
            raise ValueError("FABRIC_DATA_AGENT_URL is not configured.")
        self.auth_provider = auth_provider
        self.data_agent_url = data_agent_url

    def ask(self, question: str) -> Dict[str, Any]:
        bearer = self.auth_provider.get_fabric_token()

        headers = {
            "Authorization": f"Bearer {bearer}",
            "Content-Type": "application/json"
        }

        # This payload shape is a practical placeholder.
        # If your tenant/documented endpoint requires a different body, adjust here.
        payload = {
            "messages": [
                {
                    "role": "user",
                    "content": question
                }
            ]
        }

        response = requests.post(
            self.data_agent_url,
            headers=headers,
            json=payload,
            timeout=120
        )
        response.raise_for_status()
        return response.json()
