from datetime import datetime

from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Users(Base):
    __tablename__ = "users"

    id = Column("id", String(36), primary_key=True, nullable=False)
    name = Column("name", String, nullable=False)
    created_at = Column("created_at", DateTime, default=datetime.now(), nullable=False)
    # Because Cloud Spanner emulator does not infer null of Datatime, needs to set dummy value even if just creation
    updated_at = Column("updated_at", DateTime, default=datetime.fromtimestamp(0), onupdate=datetime.now(), nullable=False)
    scores = relationship("Scores", backref="users")


class Scores(Base):
    __tablename__ = "scores"

    id = Column("id", String(36), primary_key=True, nullable=False)
    score = Column("score", Integer, nullable=False)
    user_id = Column("user_id", String(36), ForeignKey("users.id"), nullable=False)
    created_at = Column("created_at", DateTime, default=datetime.now(), nullable=False)
    # Because Cloud Spanner emulator does not infer null of Datatime, needs to set dummy value even if just creation
    updated_at = Column("updated_at", DateTime, default=datetime.fromtimestamp(0), onupdate=datetime.now(), nullable=False)

    # For Spanner interleave test
    # spanner_interleave_in = "users",
    # spanner_interleave_on_delete_cascade = True,
