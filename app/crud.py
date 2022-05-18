# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import uuid

from sqlalchemy import desc
from sqlalchemy.orm import Session

from app import models, schemas


def get_user(db: Session, user_id: str):
    return db.query(models.Users).filter(models.Users.user_id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 1000):
    # read-only transaction
    # db.connection(execution_options={"read_only": True})
    return db.query(models.Users).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UsersBase):
    db_user = models.Users(user_id=str(uuid.uuid4()), name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: str, user: schemas.UsersBase):
    db_user = db.query(models.Users).filter(models.Users.user_id == user_id).first()
    db_user.name = user.name
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: str):
    db_user = db.query(models.Users).filter(models.Users.user_id == user_id).first()
    db.delete(db_user)
    db.commit()
    return


def get_score(db: Session, score_id: str):
    db_score = db.query(
        models.Scores.score_id.label("score_id"),
        models.Scores.score.label("score"),
        models.Scores.created_at.label("created_at"),
        models.Scores.updated_at.label("updated_at"),
        models.Users.user_id.label("user_id"),
        models.Users.name.label("user_name")).\
        join(models.Users, models.Scores.user_id == models.Users.user_id).\
        filter(models.Scores.score_id == score_id).first()
    return db_score


def get_scores(db: Session, base_score: int = 9000, skip: int = 0, limit: int = 1000):
    """
    SELECT
      scores.score_id AS score_id,
      scores.score AS score,
      scores.created_at AS created_at,
      scores.updated_at AS updated_at,
      users.user_id AS user_id,
      users.name AS user_name
    FROM
      scores @{FORCE_INDEX=ix_scores_score}
    JOIN
      users
    ON
      scores.user_id = users.user_id
    WHERE
      scores.score >= 9000
    ORDER BY
      scores.score DESC
    LIMIT
      1000
    OFFSET
      0
    """
    db_scores = db.query(
        models.Scores.score_id.label("score_id"),
        models.Scores.score.label("score"),
        models.Scores.created_at.label("created_at"),
        models.Scores.updated_at.label("updated_at"),
        models.Users.user_id.label("user_id"),
        models.Users.name.label("user_name")).\
        join(models.Users, models.Scores.user_id == models.Users.user_id).\
        filter(models.Scores.score >= base_score).\
        order_by(desc(models.Scores.score)).\
        with_hint(selectable=models.Scores, text="@{FORCE_INDEX=ix_scores_score}").\
        offset(skip).limit(limit).all()
    return db_scores


def create_score(db: Session, score: schemas.ScoresBase):
    db_score = models.Scores(user_id=score.user_id, score_id=str(uuid.uuid4()), score=score.score)
    db.add(db_score)
    db.commit()
    db.refresh(db_score)
    return db_score


def update_score(db: Session, score_id: str, score: schemas.ScoresBase):
    db_score = db.query(models.Scores).filter(models.Scores.score_id == score_id).first()
    db_score.score = score.score
    db_score.user_id = score.user_id
    db.commit()
    db.refresh(db_score)
    return db_score


def delete_score(db: Session, score_id: str):
    db_user = db.query(models.Scores).filter(models.Scores.score_id == score_id).first()
    db.delete(db_user)
    db.commit()
    return
