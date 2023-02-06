from ..model.BaseUser import BaseUser
from sqlalchemy.orm import Session
from ..auth.authenticate import AuthHandler


def login(user: BaseUser,  secret: str, lifetime_seconds: int):
    authhandler = AuthHandler(secret, lifetime_seconds)

    _payload = {}
    for key in user.payload:
        _payload[key] = user[key]
        
    token = authhandler.encode_login_token(payload=_payload)


    return token
