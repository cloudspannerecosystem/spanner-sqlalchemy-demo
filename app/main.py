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

import sys
from os import environ

from fastapi import Depends, FastAPI, HTTPException, Response, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import SessionLocal

CLOUD_RUN_SERVICE = environ.get("K_SERVICE", "")
CLOUD_RUN_REVISION = environ.get("K_REVISION", "")

app = FastAPI(docs_url="/")

# to supress the known error's stack trace
# https://github.com/googleapis/python-spanner-sqlalchemy/issues/192
sys.tracebacklimit = 0


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health/")
def read_health():
    return {"health": "true"}


@app.get("/cloud-run-info/")
def read_cloud_run_info():
    return {"service": CLOUD_RUN_SERVICE, "revision": CLOUD_RUN_REVISION}


@app.get("/users/", response_model=list[schemas.Users])
def read_users(skip: int = 0, limit: int = 1000, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}/", response_model=schemas.Users)
def read_user(user_id: str, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/", status_code=201, response_model=schemas.Users)
def create_user(user: schemas.UsersBase, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)


@app.put("/users/{user_id}/", response_model=schemas.Users)
def update_user(user_id: str, user: schemas.UsersBase, db: Session = Depends(get_db)):
    return crud.update_user(db=db, user_id=user_id, user=user)


@app.delete("/users/{user_id}/")
def delete_user(user_id: str, db: Session = Depends(get_db)):
    crud.delete_user(db=db, user_id=user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get("/scores/", response_model=list[schemas.Scores])
def read_scores(skip: int = 0, limit: int = 1000, db: Session = Depends(get_db)):
    scores = crud.get_scores(db, skip=skip, limit=limit)
    return scores


@app.get("/scores/{score_id}/", response_model=schemas.Scores)
def read_score(score_id: str, db: Session = Depends(get_db)):
    db_score = crud.get_score(db, score_id=score_id)
    if db_score is None:
        raise HTTPException(status_code=404, detail="Score not found")
    return db_score


@app.post("/scores/", status_code=201, response_model=schemas.Scores)
def create_score(score: schemas.ScoresBase, db: Session = Depends(get_db)):
    return crud.create_score(db=db, score=score)


@app.put("/scores/{score_id}/", response_model=schemas.Scores)
def update_score(score_id: str, score: schemas.ScoresBase, db: Session = Depends(get_db)):
    return crud.update_score(db=db, score_id=score_id, score=score)


@app.delete("/scores/{score_id}/", status_code=204)
def delete_score(score_id: str, db: Session = Depends(get_db)):
    crud.delete_score(db=db, score_id=score_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
