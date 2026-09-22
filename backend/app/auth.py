from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

import bcrypt
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, Field

from app.config import settings

security = HTTPBearer(auto_error=False)


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6, max_length=128)


class UserOut(BaseModel):
    username: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserStore:
    _users: dict[str, dict[str, Any]] = {}

    @classmethod
    def create_user(cls, username: str, password: str) -> dict[str, Any]:
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        user = {"username": username, "password": hashed}
        cls._users[username] = user
        return user

    @classmethod
    def get_user(cls, username: str) -> dict[str, Any] | None:
        return cls._users.get(username)

    @classmethod
    def verify_password(cls, username: str, password: str) -> bool:
        user = cls.get_user(username)
        if not user:
            return False
        return bcrypt.checkpw(password.encode(), user["password"].encode())


def create_access_token(username: str) -> str:
    expires = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    payload = {"sub": username, "exp": expires}
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> UserOut:
    if credentials is None or not credentials.scheme.lower() == "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        payload = jwt.decode(credentials.credentials, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        username = payload.get("sub")
    except jwt.PyJWTError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc

    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user = UserStore.get_user(str(username))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return UserOut(username=user["username"])
