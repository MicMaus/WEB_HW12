from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from starlette import status

from dependencies.db import get_db
from typing import Optional
from repository import auth as repository_auth


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "secret_key"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_connected_client(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode JWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload["scope"] == "access_token":
            email = payload["sub"]
            if email is None:
                raise credentials_exception
        else:
            raise credentials_exception
    except JWTError as e:
        raise credentials_exception

    user = repository_auth.get_user_by_email(email, db)
    if user is None:
        raise credentials_exception
    return user


def verify_password(self, plain_password, hashed_password):
    return self.pwd_context.verify(plain_password, hashed_password)


def get_password_hash(self, password: str):
    return self.pwd_context.hash(password)


# define a function to generate a new access token
def create_access_token(self, data: dict, expires_delta: Optional[float] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + timedelta(seconds=expires_delta)
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"iat": datetime.utcnow(), "exp": expire, "scope": "access_token"})
    encoded_access_token = jwt.encode(
        to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM
    )
    return encoded_access_token


# define a function to generate a new refresh token
def create_refresh_token(self, data: dict, expires_delta: Optional[float] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + timedelta(seconds=expires_delta)
    else:
        expire = datetime.utcnow() + timedelta(days=7)
    to_encode.update(
        {"iat": datetime.utcnow(), "exp": expire, "scope": "refresh_token"}
    )
    encoded_refresh_token = jwt.encode(
        to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM
    )
    return encoded_refresh_token


def decode_refresh_token(self, refresh_token: str):
    try:
        payload = jwt.decode(
            refresh_token, self.SECRET_KEY, algorithms=[self.ALGORITHM]
        )
        if payload["scope"] == "refresh_token":
            email = payload["sub"]
            return email
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid scope for token",
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
