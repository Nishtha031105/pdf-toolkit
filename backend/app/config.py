import os
import secrets
from dataclasses import dataclass, field
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
STORAGE_DIR = BASE_DIR / "storage"


def _load_jwt_secret() -> str:
    value = os.getenv("JWT_SECRET")
    if value:
        return value
    STORAGE_DIR.mkdir(parents=True, exist_ok=True)
    secret_file = STORAGE_DIR / "jwt_secret.txt"
    if not secret_file.exists():
        secret_file.write_text(secrets.token_urlsafe(48), encoding="utf-8")
    return secret_file.read_text(encoding="utf-8").strip()


@dataclass(frozen=True)
class Settings:
    app_name: str = "PDF Toolkit API"
    cors_origins: tuple[str, ...] = (
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:4173",
        "http://127.0.0.1:4173",
    )
    database_path: Path = STORAGE_DIR / "app.db"
    jwt_secret: str = field(default_factory=_load_jwt_secret)
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 12
    max_file_size_mb: int = 50
    max_total_upload_mb: int = 200
    max_files_per_request: int = 50
    max_preview_pages: int = 300
    max_split_outputs: int = 200
    thumbnail_width: int = 200

    @property
    def max_file_size_bytes(self) -> int:
        return self.max_file_size_mb * 1024 * 1024

    @property
    def max_total_upload_bytes(self) -> int:
        return self.max_total_upload_mb * 1024 * 1024


settings = Settings()
