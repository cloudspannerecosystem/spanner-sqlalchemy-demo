import uuid

from sqlalchemy.orm import Session
from app import models, schemas


def get_user(db: Session, user_id: str):
    return db.query(models.Users).filter(models.Users.id == user_id).first()


def get_users(db: Session,  skip: int = 0, limit: int = 1000):
    # read-only transaction
    # db.connection(execution_options={"read_only": True})
    return db.query(models.Users).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UsersBase):
    db_user = models.Users(id=str(uuid.uuid4()), name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: str, user: schemas.UsersBase):
    db_user = db.query(models.Users).filter(models.Users.id == user_id).first()
    db_user.name = user.name
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: str):
    db_user = db.query(models.Users).filter(models.Users.id == user_id).first()
    db.delete(db_user)
    db.commit()
    return


def get_score(db: Session, score_id: str):
    return db.query(models.Scores).filter(models.Scores.id == score_id).first()


def get_scores(db: Session,  skip: int = 0, limit: int = 1000):
    return db.query(models.Scores).offset(skip).limit(limit).all()


def create_score(db: Session, score: schemas.ScoresBase):
    db_score = models.Scores(id=str(uuid.uuid4()), score=score.score, user_id=score.user_id)
    db.add(db_score)
    db.commit()
    db.refresh(db_score)
    return db_score


def update_score(db: Session, score_id: str, score: schemas.ScoresBase):
    db_score = db.query(models.Scores).filter(models.Scores.id == score_id).first()
    db_score.score = score.score
    db_score.user_id = score.user_id
    db.commit()
    db.refresh(db_score)
    return db_score


def delete_score(db: Session, score_id: str):
    db_user = db.query(models.Scores).filter(models.Scores.id == score_id).first()
    db.delete(db_user)
    db.commit()
    return
