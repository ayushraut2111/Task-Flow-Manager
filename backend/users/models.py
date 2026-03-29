from sqlalchemy import String
from sqlalchemy.orm import Mapped,mapped_column, relationship
from core.utils import get_random_id
from core.models import BaseModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from boards.models import Board,Card

class User(BaseModel):
    __tablename__="users"

    username: Mapped[str | None] = mapped_column(
        String(255), unique=True, index=True)
    name : Mapped[str] = mapped_column(String(255))
    phone :Mapped[str] = mapped_column(String(20),unique=True,index=True)
    email :Mapped[str| None]=mapped_column(String(50),nullable=True)
    is_active :Mapped[bool]=mapped_column(default=True)
    boards : Mapped[list["Board"]]=relationship(back_populates="owner",passive_deletes=True)
    cards: Mapped[list["Card"]] = relationship(
        back_populates="assigned_to", passive_deletes=True)



    def save(self, db):
        if not self.username:
            self.username = get_random_id("U")
        return super().save(db)