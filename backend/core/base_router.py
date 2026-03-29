from fastapi import APIRouter
from users.routes import router as user_router

router = APIRouter()

router.include_router(
    user_router, prefix="/users", tags=["User"]
)
