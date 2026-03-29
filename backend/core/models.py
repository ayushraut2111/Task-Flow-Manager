from sqlalchemy.orm import Mapped, mapped_column
import uuid
from datetime import datetime
from sqlalchemy import func
from core.database import Base
from slugify import slugify


class BaseModel(Base):
    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())

    def save(self, db):
        db.add(self)
        db.commit()
        db.refresh(self)
        return self


class SlugBaseModel(BaseModel): 
    __abstract__ = True

    slug: Mapped[str] = mapped_column(unique=True, index=True)

    def save(self, db):
        if not hasattr(self, "name") or not self.name:
            raise ValueError("name is required to generate slug")
        self.slug = slugify(self.name)
        return super().save(db)
