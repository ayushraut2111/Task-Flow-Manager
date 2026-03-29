from datetime import datetime, timedelta
from jose import jwt
from core.config import settings


class JWTTokenAuth:
    def __init__(self):
        self.access_token_expire_minutes=30
        self.refresh_token_expire_minutes=7
        self.algorithm = "HS256"
        self.secret_key=settings.JWT_AUTH_SECRET_KEY

    def create_access_token(self,user_id: str) -> str:
        expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        return jwt.encode({"user_id": user_id, "exp": expire, "type": "access"}, self.secret_key, algorithm=self.algorithm)


    def create_refresh_token(self,user_id: str) -> str:
        expire = datetime.utcnow() + timedelta(days=self.refresh_token_expire_minutes)
        return jwt.encode({"user_id": user_id, "exp": expire, "type": "refresh"}, self.secret_key, algorithm=self.algorithm)


    def decode_token(self,token: str) -> dict:
        return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
