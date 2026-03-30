from fastapi import APIRouter
from users.routes import router as user_router
from boards.routes import router as board_router

router = APIRouter()

router.include_router(
    user_router, prefix="/users", tags=["User"]
)

router.include_router(
    board_router, prefix="/boards", tags=["Board"]
)
