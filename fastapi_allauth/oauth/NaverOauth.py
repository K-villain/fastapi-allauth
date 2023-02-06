from typing import Optional, List, Dict, Any
import requests
from . import BaseOauth

AUTH_URL = "https://nid.naver.com/oauth2.0/authorize"
TOKEN_URL = "https://nid.naver.com/oauth2.0/token"
USER_INFO_URL = "https://openapi.naver.com/v1/nid/me"


class NaverOauth(BaseOauth.BaseOauth):

    def __init__(
        self,
        provider: str = "NAVER",
        client_id: str = "",
        client_secret: str = "",
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
        response = requests.get(USER_INFO_URL, headers={
                                "Authorization": f"Bearer {access_token}"})
        return response.json()

    def get_open_id(self, user_json: dict):
        return user_json["response"]["id"]
