import sqlite3
from dataclasses import dataclass
from app.database import get_connection
from app.errors import AppError
from app.security import hash_password, verify_password

_DUMMY_HASH = hash_password("not-a-real-password")

@dataclass(frozen=True)
class User:
    id: int
    username: str

def create_user(username: str, password: str) -> User:
    try:
        with get_connection() as connection:
            cursor = connection.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, hash_password(password)))
            return User(id=cursor.lastrowid, username=username)
    except sqlite3.IntegrityError:
        raise AppError("That username is already taken.", 409) from None

def get_user_by_id(user_id: int) -> User | None:
    with get_connection() as connection:
        row = connection.execute("SELECT id, username FROM users WHERE id = ?", (user_id,)).fetchone()
    return User(id=row["id"], username=row["username"]) if row else None

def authenticate(username: str, password: str) -> User | None:
    with get_connection() as connection:
        row = connection.execute("SELECT id, username, password_hash FROM users WHERE username = ?", (username,)).fetchone()
    if row is None:
        verify_password(password, _DUMMY_HASH)
        return None
    if not verify_password(password, row["password_hash"]):
        return None
    return User(id=row["id"], username=row["username"])
