from fastapi import APIRouter, Depends
from sqlalchemy import select
from boards.schemas import CreateBoardSchema, BoardSchema
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from users.authentication import get_current_user
from users.models import User
from fastapi.responses import JSONResponse
from boards.models import Board

router = APIRouter()
board_router = APIRouter()


@board_router.post("/")
async def create_board_api(data: CreateBoardSchema, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    # first check whether board with same name exist for a same user, if not then create otherwise send error
    board_result = await db.execute(select(Board).where(
        Board.name == data.name and Board.owner_id == current_user.id))

    board = board_result.scalar_one_or_none()

    if board:
        return JSONResponse(content={"message": "Board already present"}, status_code=400)

    board = Board(
        name=data.name,
        description=data.description,
        owner_id=current_user.id
    )
    await board.save(db)

    return JSONResponse(content={"message": "Board Created Successfully"}, status_code=200)


@board_router.get("/", response_model=list[BoardSchema], status_code=200)
async def get_all_boards_api(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    boards_results = await db.execute(select(Board).where(Board.owner_id == current_user.id))

    boards = boards_results.scalars().all()

    return boards


router.include_router(board_router, prefix="/board", tags=["BoardApi"])
