from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.security import decode_access_token
from app.services.user_service import User, get_user_by_id

bearer_scheme = HTTPBearer(auto_error=False)

def get_current_user(credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme)) -> User:
    user = None
    if credentials is not None:
        user_id = decode_access_token(credentials.credentials)
        if user_id is not None:
            user = get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="Your session has expired. Please log in again.", headers={"WWW-Authenticate": "Bearer"})
    return user
