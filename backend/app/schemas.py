import re
from pydantic import BaseModel, Field, field_validator

class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=32)
    password: str = Field(min_length=8, max_length=128)
    @field_validator("username")
    @classmethod
    def username_characters(cls, value: str) -> str:
        if not re.fullmatch(r"[A-Za-z0-9_.-]+", value):
            raise ValueError("can only contain letters, numbers, dots, dashes and underscores")
        return value

class LoginRequest(BaseModel):
    username: str = Field(max_length=64)
    password: str = Field(max_length=128)

class UserResponse(BaseModel):
    id: int
    username: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class PdfInfoResponse(BaseModel):
    filename: str
    page_count: int

class PagePreviewsResponse(BaseModel):
    page_count: int
    pages: list[str]
