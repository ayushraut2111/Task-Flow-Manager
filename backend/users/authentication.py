from passlib.context import CryptContext
from core.authentication import JWTTokenAuth

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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
