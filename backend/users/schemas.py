from pydantic import BaseModel


class RegisterSchema(BaseModel):
    name: str
    phone: str
    email: str | None = None
    password: str


class LoginSchema(BaseModel):
    phone: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshSchema(BaseModel):
    refresh_token: str
