## Params
`allauth_manager` takes in the following parameters in its constructor.

- `db`: a SQLAlchemy session object that is used for interacting with a database.
- `user`: a user object that inherits `BaseUser`.
- `secret`: a string that is used to encrypt and decrypt JSON web tokens (JWT).
- `lifetime_second`: an integer representing the lifetime in seconds of a token.

## Methods
`allauth_manager` provides the following methods.

- `get_oauth_router`: a method that returns an instance of FastAPI's APIRouter with two endpoints, `/authorize` and `/callback`, for handling OAuth authorization and callback processes, respectively.
    - **/authorize**

        - **Description**: This endpoint is returns a JSON response containing authorization url

        - **Headers**:

            - Content-Type: `application/json`

        - **Request Body**:

            - scope: string

        - **Response Body**:

            - url: string (required)

        - **Response Status Codes**:

            - 200 OK: return url was successful 
            - 400 Bad Request: Required parameters are missing or invalid.

        - **Example Request**:

            ```
            bashCopy codePOST /authorize
            Content-Type: application/json

            {
                "scope": "email, birth"
            }
            ```
            
    - **/callback**

        - **Description**: This endpoint is used for logging into the system. It returns a JSON response containing access and refresh tokens.

        - **Headers**:

        - **Content-Type**: `application/json`

        **Request Body**:

            - code: string (required)
            - state: string (required)

        **Response Body**:

            - access_token: string (required)
            - refresh_token: string (required)

        **Response Status Codes**:

            - 200 OK: Login was successful and access and refresh tokens are returned in the response.
            - 400 Bad Request: Required parameters are missing or invalid.
            - 401 Unauthorized: Incorrect email or password.

        **Example Request**:

            ```
            bashCopy codePOST /login
            Content-Type: application/json

            {
                "code": "code",
                "state": "state"
            }
            ```

        **Example Response**:

            ```
            cssCopy codeHTTP/1.1 200 OK
            Content-Type: application/json

            {
                "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1ODk5MTk0MDUsImlhdCI6MTU4OTkxODkwNSwiZW1haWwiOiJleGFtcGxlQGdtYWlsLmNvbSJ9.iQ21xFyE0NlNlZ6Wxdu8UOhN1rLjKlFcNbLKj0vL-4I",
                "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1OTA1MjQyMDUsImlhdCI6MTU4OTkxODkwNSwiZW1haWwiOiJleGFtcGxlQGdtYWlsLmNvbSJ9.NxL-yaCnS1SzfIgWU6BQik6DJj9PiYbZ6fmgW8pv068",
                "expires_in": 86400
            }
            ```

- `login_required`: a decorator that checks if a user is logged in. If the user is not logged in or the token is invalid, it raises a `HTTPException` with status code 401.


## Code

```py
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from oauth.BaseOauth import BaseOauth
from auth import login, register, AuthHandler
from model import BaseUser
from functools import wraps


class AllauthManager:
    db: Session
    user: BaseUser
    secret: str
    lifetime_second: int = 3600

    def __init__(self, db, user, secret, lifetime_second) -> None:
        self.db = db
        self.user = user
        self.secret = secret
        self.lifetime_second = lifetime_second

    def get_oauth_router(self, oauth: BaseOauth) -> APIRouter:

        router = APIRouter()

        @router.get("/authorize")
        async def authorize(scope: Optional[str] = None):
            url = await oauth.get_authorization_url(scope=scope)
            return {"url": url}

        @router.get("/callback")
        async def callback(code: Optional[str] = None, state: Optional[str] = None):
            tokens = await oauth.get_access_token(code=code, state=state)
            user_json = oauth.get_userinfo(tokens["access_token"])
            _user = self.user.create(
                open_id=oauth.get_open_id(user_json=user_json), provider=oauth.provider)

            if self.get_user_by_authority(_user.authority) is None:
                try:
                    register(self.db , _user)
                except Exception("Register failed"):
                    pass

            return login(_user, self.secret, self.lifetime_second)

        return router

    def get_user_by_authority(self, authority: str):
        return self.db.query(BaseUser).filter(BaseUser.authority == authority).first()


    def login_required(self, func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            auth_handler = AuthHandler(self.secret, self.lifetime_second)
            token = kwargs.get('authorization', False)
            if token :
                authority = auth_handler.decode_access_token(token)

                if not self.get_user_by_authority(authority) :
                    raise HTTPException(status_code=401, detail="user not exist")

            else:
                raise HTTPException(status_code=401, detail="token required")

            # success
            return await func(*args, **kwargs)

        return wrapper
```



