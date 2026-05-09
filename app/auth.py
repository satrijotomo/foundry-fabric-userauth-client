from azure.identity import InteractiveBrowserCredential


class UserAuth:
    """
    Interactive end-user authentication via Microsoft Entra ID.

    Microsoft documents interactive browser authentication for external
    Python applications consuming Fabric data agents.
    """

    def __init__(self, tenant_id: str):
        self.credential = InteractiveBrowserCredential(tenant_id=tenant_id)

    def get_foundry_token(self) -> str:
        """
        Token for calling Foundry agent endpoints.
        """
        token = self.credential.get_token("https://ai.azure.com/.default")
        return token.token

    def get_fabric_token(self) -> str:
        """
        Token for calling Fabric REST-backed endpoints directly.
        """
        token = self.credential.get_token("https://api.fabric.microsoft.com/.default")
        return token.token