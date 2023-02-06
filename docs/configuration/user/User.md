# User

## BaseUser
`BaseUser` is a SQLAlchemy based model which represents a user in a database.

- `id` : a UUID representing the unique identifier of a user.
- `authority` : a SHA256 hash of the user's open_id and provider.

```py
from pydantic import BaseModel, Field, constr
from sqlalchemy import Column, String
import hashlib
import uuid

class BaseUser(Base):

    __tablename__ = "User"

    id = Column(String, primary_key=True, index=True)
    authority = Column(String)

    payload = {
    }

    def __init__(self, id, authority):
        self.id = id
        self.authority = authority

    @classmethod
    def create_authority(cls, open_id, provider):
        context = str(open_id)+provider
        authority = hashlib.sha256(context.encode()).hexdigest()
        return authority

    @classmethod
    def create(
        cls,
        open_id: String,
        provider: String,
    ):
        authority = cls.create_authority(open_id, provider)
        id = uuid.uuid4().hex

        return cls(id=id, authority=authority)

    class Config:
        orm_mode = True

```

## CustomUser
`CustomUser` is a optional class which inherits `BaseUser`.
If you want to add new columns or payload, you can write it as follows.

```py
from fastapi_allauth.model import BaseUser
from sqlalchemy import Column, String

class CustomUser(BaseUser):
    # defalut payload only has an ID
    # update your payload
    payload = {
        "custom": "custom"
        ... 
    }

    # If additional columns are needed, add them.

```