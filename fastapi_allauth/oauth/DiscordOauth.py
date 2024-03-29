from typing import Optional, List, Dict, Any
import requests
from . import BaseOauth
from secret_handler import SecretType


AUTH_URL = "https://discord.com/api/oauth2/authorize"
TOKEN_URL = "https://discord.com/api/v10/oauth2/token"
USER_INFO_URL = "https://discord.com/api/users/@me"


class DiscordOauth(BaseOauth.BaseOauth):

    def __init__(
        self,
        provider: str = "DISCORD",
        client_id: str = "",
        client_secret: SecretType = "",
        redirect_uri: str = "",
        scope: Optional[List[str]] = None,
        refresh_token_url: Optional[str] = None,
        revoke_token_url: Optional[str] = None
    ):
        super().__init__(
            provider=provider,
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            authorize_url=AUTH_URL,
            access_token_url=TOKEN_URL,
            base_scope=scope,
            refresh_token_url=refresh_token_url,
            revoke_token_url=revoke_token_url
        )

    def get_userinfo(self, access_token: str):
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(USER_INFO_URL, headers=headers)
        return response.json()

    def get_open_id(self, user_json: dict):
        return user_json["id"]
