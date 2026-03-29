from fastapi import APIRouter, Depends
from sqlalchemy import select
from core.authentication import JWTTokenAuth
from users.authentication import hash_password
from users.models import User
from users.schemas import LoginSchema, RegisterSchema, TokenResponse
from core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse
from typing import Union
from users.authentication import verify_password

router = APIRouter()
auth_router = APIRouter()


@auth_router.post("/register", status_code=201)
async def user_register_api(data: RegisterSchema, db: AsyncSession = Depends(get_db)):

    result = await db.execute(select(User).where(User.phone == data.phone))

    if result.scalar_one_or_none():
        return JSONResponse(content={"message": "Phone number is already registered"}, status_code=400)

    user = User(
        name=data.name,
        phone=data.phone,
        email=data.email,
        password=hash_password(data.password)
    )

    await user.save(db)
    return JSONResponse(content={"message": "User registered successfully"}, status_code=201)


@auth_router.post("/login", status_code=200, response_model=Union[TokenResponse, dict])
async def user_login_api(data: LoginSchema, db: AsyncSession = Depends(get_db)):

    jwt_token_auth = JWTTokenAuth()

    # first check the user with this phone exist or not
    usr_result = await db.execute(select(User).where(User.phone == data.phone))
    user = usr_result.scalar_one_or_none()

    if not user:
        return JSONResponse(content={"message": "User with this phone number not found"}, status_code=400)

    if not verify_password(data.password, user.password):
        return JSONResponse(content={"message": "Invalid Password"}, status_code=400)

    return TokenResponse(access_token=jwt_token_auth.create_access_token(str(user.id)), refresh_token=jwt_token_auth.create_refresh_token(str(user.id)))

router.include_router(
    auth_router,
    prefix="/auth",
    tags=["Auth"]
)
