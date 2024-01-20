from schemas.client import ClientPydant, TokenPydant
from repository import auth as repository_auth
from fastapi import HTTPException, status, Security, Depends, APIRouter

from fastapi.security import (
    OAuth2PasswordRequestForm,
    HTTPAuthorizationCredentials,
    HTTPBearer,
)

from services.auth import auth_service

from sqlalchemy.orm import Session
from dependencies.db import get_db

from schemas.client import ClientPydant, ClientResponsePydant

router = APIRouter()  # tags=["auth"]
security = HTTPBearer()


@router.post(
    "/signup", response_model=ClientResponsePydant, status_code=status.HTTP_201_CREATED
)
def signup(body: ClientPydant, db: Session = Depends(get_db)):
    exist_user = repository_auth.get_user_by_email(body.email, db)
    if exist_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Account already exists"
        )
    body.password = auth_service.get_password_hash(body.password)
    new_user = repository_auth.create_user(body, db)
    return ClientResponsePydant(user=new_user, detail="User successfully created")


@router.post("/login", response_model=TokenPydant)
def login(body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = repository_auth.get_user_by_email(body.username, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email"
        )
    if not auth_service.verify_password(body.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password"
        )
    # Generate JWT
    access_token = auth_service.create_access_token(data={"sub": user.email})
    refresh_token = auth_service.create_refresh_token(data={"sub": user.email})
    repository_auth.update_token(user, refresh_token, db)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.get("/refresh_token", response_model=TokenPydant)
def refresh_token(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    token = credentials.credentials
    email = auth_service.decode_refresh_token(token)
    user = repository_auth.get_user_by_email(email, db)
    if user.refresh_token != token:
        repository_auth.update_token(user, None, db)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )

    access_token = auth_service.create_access_token(data={"sub": email})
    refresh_token = auth_service.create_refresh_token(data={"sub": email})
    repository_auth.update_token(user, refresh_token, db)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }
