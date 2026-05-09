import requests
from typing import Any, Dict, Optional


class FoundryAgentClient:
    def __init__(self, auth_provider, responses_url: str, activity_url: str):
        self.auth_provider = auth_provider
        self.responses_url = responses_url
        self.activity_url = activity_url

    def call_responses(
        self,
        user_input: str,
        conversation_id: Optional[str] = None
    ) -> Dict[str, Any]:

        bearer = self.auth_provider.get_foundry_token()

        headers = {
            "Authorization": f"Bearer {bearer}",
            "Content-Type": "application/json",
            "Foundry-Features": "HostedAgents=V1Preview"
        }

        payload: Dict[str, Any] = {
            "input": [
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": user_input}
                    ]
                }
            ],
            "store": True
        }

        # ✅ ONLY send conversation if valid
        if conversation_id:
            payload["conversation"] = {"id": conversation_id}

        response = requests.post(
            self.responses_url,
            headers=headers,
            json=payload,
            timeout=120
        )

        if not response.ok:
            raise RuntimeError(
                f"Foundry call failed Status: {response.status_code} {response.text}"
            )

        return response.json()