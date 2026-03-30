from passlib.context import CryptContext
from core.authentication import JWTTokenAuth
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from users.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
bearer = HTTPBearer()


def hash_password(password: str) -> str:
    password = password.encode("utf-8")[:72].decode("utf-8", errors="ignore")
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    plain = plain.encode("utf-8")[:72].decode("utf-8", errors="ignore")
    return pwd_context.verify(plain, hashed)


def autheticate_user(token: str, token_type: str = "access"):
    jwt_token_auth = JWTTokenAuth()

    try:
        jwt_data = jwt_token_auth.decode_token(token)
    except:
        raise Exception(f"Invalid or expired {token_type} token")

    if jwt_data.get("type") != token_type:
        raise Exception("Invalid token type")

    return jwt_data


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
    db: AsyncSession = Depends(get_db)
):
    # this function authenticate and verifies user from bearer token
    token = credentials.credentials
    jwt_token_auth = JWTTokenAuth()

    try:
        payload = jwt_token_auth.decode_token(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    if payload.get("type") != JWTTokenAuth.TOKEN_TYPE_ACCESS:
        raise HTTPException(status_code=401, detail="Wrong Token Type")

    user = await db.get(User, payload.get("user_id"))

    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=401, detail="User is inactive")

    return user
