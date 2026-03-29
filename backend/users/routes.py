from fastapi import APIRouter, Depends
from core.database import get_db

router = APIRouter()
auth_router = APIRouter()


router.include_router(auth_router, prefix="/auth", tags=["Auth"])
