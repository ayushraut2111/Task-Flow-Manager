from pydantic import BaseModel
from users.schemas import UserSchema


class CreateBoardSchema(BaseModel):
    name:str
    description:str | None


class BoardSchema(BaseModel):
    slug : str
    name:str
    description :str |None
    is_deleted :bool
    owner: UserSchema
