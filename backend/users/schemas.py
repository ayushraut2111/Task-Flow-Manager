from pydantic import BaseModel, field_validator, EmailStr
import re

class RegisterSchema(BaseModel):
    name: str
    phone: str
    email: EmailStr | None = None
    password: str

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        phone = v.strip()
        phone = re.sub(r"[\s\-\(\)]", "", phone)
        phone = re.sub(r"^\+?0{0,2}91", "", phone)

        if not re.fullmatch(r"\d{10}", phone):
            raise ValueError("Invalid phone number")

        return phone



class LoginSchema(BaseModel):
    phone: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

    class Config:
        from_attributes = True


class RefreshSchema(BaseModel):
    refresh_token: str
