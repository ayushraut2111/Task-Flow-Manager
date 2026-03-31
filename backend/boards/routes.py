import uuid
from fastapi import APIRouter, Depends
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload, joinedload
from boards.schemas import CreateBoardSchema, BoardSchema, BoardUpdateSchema
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from users.authentication import get_current_user
from users.models import User
from fastapi.responses import JSONResponse
from boards.models import Board, TaskList, Card
from typing import Union

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
    boards_results = await db.execute(select(Board).where(Board.owner_id == current_user.id, Board.is_deleted == False))

    boards = boards_results.scalars().all()

    return boards


@board_router.get("/{board_id}", response_model=Union[BoardSchema, dict], status_code=200)
async def get_single_board_api(board_id: uuid.UUID, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Board)
        .where(
            Board.id == board_id,
            Board.owner_id == current_user.id,
            Board.is_deleted == False
        )
        .options(
            selectinload(Board.lists)
            .selectinload(TaskList.cards)
        )
    )
    board = result.scalar_one_or_none()

    if not board:
        return JSONResponse(content={"message": "Board not found"}, status_code=400)

    return board


@board_router.delete("/{board_id}")
async def delete_a_board_api(board_id: uuid.UUID, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Board)
        .where(
            Board.id == board_id,
            Board.owner_id == current_user.id,
            Board.is_deleted == False
        )
    )
    board = result.scalar_one_or_none()

    if not board:
        return JSONResponse(content={"message": "Board not found"}, status_code=400)

    board.is_deleted = True
    await board.save(db)

    # also delete their lists and cards

    await db.execute(
        update(TaskList)
        .where(TaskList.board_id == board_id)
        .values(is_deleted=True)
    )
    await db.execute(
        update(Card)
        .where(Card.list_id.in_(
            select(TaskList.id).where(TaskList.board_id == board_id)
        ))
        .values(is_deleted=True)
    )

    return JSONResponse(
        content={"message": "Board deleted successfully"}, status_code=200
    )


@board_router.patch("/{board_id}", response_model=BoardSchema, status_code=200)
async def update_board_api(board_id: uuid.UUID, data: BoardUpdateSchema,
                           current_user: User = Depends(get_current_user),
                           db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Board).where(
            Board.id == board_id,
            Board.owner_id == current_user.id,
            Board.is_deleted == False
        )
        .options(
            joinedload(Board.owner),
            selectinload(Board.lists)
            .selectinload(TaskList.cards)
        )
    )
    board = result.scalar_one_or_none()

    if not board:
        return JSONResponse(content={"message": "Board not found"}, status_code=400)

    # get only fields that are sent and not null (exclude unset)
    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        if value is not None:
            setattr(board, key, value)

    await board.save(db)

    return board


router.include_router(board_router, prefix="/board", tags=["BoardApi"])

# only make create and update api for list and delete, and put that everything in get board api
