import uuid

from pydantic import BaseModel, ConfigDict, EmailStr


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    display_name: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class CurrentUser(BaseModel):
    model_config = ConfigDict(
        frozen=True,
    )
    user_id: uuid.UUID
    organization_id: uuid.UUID
    email: EmailStr
    display_name: str
    roles: tuple[str, ...]
