from schemas.client import ClientPydant
from fastapi import HTTPException, status, Security, Depends, APIRouter

from fastapi.security import (
    OAuth2PasswordRequestForm,
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from services.auth import (
    create_access_token,
    create_refresh_token,
    get_current_user,
    get_email_form_refresh_token,
    Hash,
)

from sqlalchemy.orm import Session
from dependencies.db import get_db
from models import user

from models.client import ClientDB

router = APIRouter()
hash_handler = Hash()
security = HTTPBearer()


@router.post("/signup")
def signup(body: ClientPydant, db: Session = Depends(get_db)):
    exist_client = db.query(ClientDB).filter(ClientDB.email == body.email).first()
    if exist_client:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Account already exists"
        )
    new_user = ClientDB(
        email=body.email, password=hash_handler.get_password_hash(body.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"new_user": new_user.email}


@router.post("/login")
def login(body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    client = (
        db.query(ClientDB).filter(ClientDB.email == body.username).first()
    )  # email is used as username
    if client is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email"
        )
    if not hash_handler.verify_password(body.password, client.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password"
        )
    # Generate JWT
    access_token = create_access_token(data={"sub": client.email})
    refresh_token = create_refresh_token(data={"sub": client.email})
    client.refresh_token = refresh_token
    db.commit()
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.get("/refresh_token")
def refresh_token(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    token = credentials.credentials
    email = get_email_form_refresh_token(token)
    user = db.query(ClientDB).filter(ClientDB.email == email).first()
    if user.refresh_token != token:
        user.refresh_token = None
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )

    access_token = create_access_token(data={"sub": email})
    refresh_token = create_refresh_token(data={"sub": email})
    user.refresh_token = refresh_token
    db.commit()
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.get("/")
def root():
    return {"message": "Hello World"}


@router.get("/secret")
def read_item(current_user: ClientDB = Depends(get_current_user)):
    return {"message": "secret router", "owner": current_user.email}
