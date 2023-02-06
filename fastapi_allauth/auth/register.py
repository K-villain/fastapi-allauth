from ..model.BaseUser import BaseUser
from sqlalchemy.orm import Session


def register(db: Session, user: BaseUser):
   
    db.add(user)
    db.commit()
    db.refresh(user)

    return user
