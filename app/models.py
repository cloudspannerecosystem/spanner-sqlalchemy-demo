from datetime import datetime

from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Users(Base):
    __tablename__ = "users"

    user_id = Column("user_id", String(36), primary_key=True, nullable=False)
    name = Column("name", String, nullable=False)
    created_at = Column("created_at", DateTime, default=datetime.now(), nullable=False)
    # Because Cloud Spanner emulator does not infer null of Datatime, needs to set dummy value even if just creation
    updated_at = Column("updated_at", DateTime, default=datetime.fromtimestamp(0), onupdate=datetime.now(), nullable=False)


class Scores(Base):
    __tablename__ = "scores"
    __table_args__ = {
        'spanner_interleave_in': 'users',
        'spanner_interleave_on_delete_cascade': True
    }

    user_id = Column("user_id", String(36), primary_key=True, nullable=False)
    score_id = Column("score_id", String(36), primary_key=True, nullable=False)
    score = Column("score", Integer, nullable=False)
    created_at = Column("created_at", DateTime, default=datetime.now(), nullable=False)
    # Because Cloud Spanner emulator does not infer null of Datatime, needs to set dummy value even if just creation
    updated_at = Column("updated_at", DateTime, default=datetime.fromtimestamp(0), onupdate=datetime.now(), nullable=False)

Scores.__table__.add_is_dependent_on(Users.__table__)