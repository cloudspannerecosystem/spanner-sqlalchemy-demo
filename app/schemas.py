from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class UsersBase(BaseModel):
    name: str


class Users(UsersBase):
    user_id: str
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class ScoresBase(BaseModel):
    score: int
    user_id: str


class Scores(ScoresBase):
    score_id: str
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
