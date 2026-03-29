import uuid
from core.models import SlugBaseModel
from sqlalchemy.orm import Mapped,mapped_column, relationship
from sqlalchemy import String,ForeignKey
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from users.models import User

class Board(SlugBaseModel):
    __tablename__="boards"

    name: Mapped[str] = mapped_column(String(255))
    description:Mapped[str|None] = mapped_column()
    is_deleted: Mapped[bool] = mapped_column(default=False)
    owner_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True)
    owner :Mapped["User"] = relationship(back_populates="boards")
    lists :Mapped[list["TaskList"]]=relationship(back_populates="board",passive_deletes=True)


class TaskList(SlugBaseModel):
    __tablename__="lists"

    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column()
    is_deleted: Mapped[bool] = mapped_column(default=False)
    priority :Mapped[int|None] =mapped_column(default=0)
    board_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("boards.id",ondelete="CASCADE"),index=True)
    board :Mapped[Board]=relationship(back_populates="lists")

    cards :Mapped[list["Card"]]=relationship(back_populates="list",passive_deletes=True)

class Card(SlugBaseModel):
    __tablename__="cards"

    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column()
    is_deleted: Mapped[bool] = mapped_column(default=False)
    position :Mapped[str] = mapped_column(String(255),default="a")
    list_id :Mapped[uuid.UUID] = mapped_column(ForeignKey("lists.id",ondelete="CASCADE"),index=True)
    list: Mapped[TaskList] =relationship(back_populates="cards")

    assigned_to_id :Mapped[uuid.UUID |None ]=mapped_column(ForeignKey("users.id",ondelete="SET NULL"),index=True)
    assigned_to :Mapped["User | None"] = relationship(back_populates="cards")