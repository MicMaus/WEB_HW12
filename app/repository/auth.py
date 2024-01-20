from sqlalchemy.orm import Session

from models.client import ClientDB
from schemas.client import ClientPydant


def get_user_by_email(email: str, db: Session) -> ClientDB:
    return db.query(ClientDB).filter(ClientDB.email == email).first()


def create_user(body: ClientPydant, db: Session) -> ClientDB:
    new_user = ClientDB(**body.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def update_token(user: ClientDB, token: str | None, db: Session) -> None:
    user.refresh_token = token
    db.commit()
