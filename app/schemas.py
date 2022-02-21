from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class UsersBase(BaseModel):
    name: str


class Users(UsersBase):
    id: str
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class ScoresBase(BaseModel):
    score: int
    user_id: str


class Scores(ScoresBase):
    id: str
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
