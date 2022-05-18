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

from fastapi.testclient import TestClient

from app import models
from app.main import app

client = TestClient(app)


def test_read_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"health": "true"}


def test_read_cloud_run_info():
    # Don't forget to set env vars at your test execution environment
    # export K_SERVICE=spanner-sqlalchemy-demo
    # export K_REVISION=spanner-sqlalchemy-demo-00001-thx
    response = client.get("/cloud-run-info")
    assert response.status_code == 200
    assert response.json() == {"service": "spanner-sqlalchemy-demo", "revision": "spanner-sqlalchemy-demo-00001-thx"}


def test_read_users(test_db):
    user1 = models.Users(user_id=str(uuid.uuid4()), name="Test Taro")
    user2 = models.Users(user_id=str(uuid.uuid4()), name="Test Jiro")
    test_db.add_all([user1, user2])
    test_db.flush()
    test_db.commit()

    response = client.get("/users")

    assert response.status_code == 200
    assert response.json()[0]["name"] == "Test Jiro" or "Test Taro"


def test_read_user(test_db):
    user1 = models.Users(user_id=str(uuid.uuid4()), name="Test Taro")
    test_db.add(user1)
    test_db.flush()
    test_db.commit()
    response = client.get("/users/" + user1.user_id + "/")
    assert response.status_code == 200
    assert response.json()["name"] == "Test Taro"


def test_create_user(test_db):
    response = client.post("/users/", json={"name": "Test Taro"})
    assert response.status_code == 201
    assert response.json()["name"] == "Test Taro"


def test_update_user(test_db):
    user1 = models.Users(user_id=str(uuid.uuid4()), name="Test Taro")
    test_db.add(user1)
    test_db.flush()
    test_db.commit()
    response = client.put("/users/" + user1.user_id + "/", json={"name": "Test Jiro"})
    assert response.status_code == 200
    assert response.json()["name"] == "Test Jiro"


def test_delete_user(test_db):
    user1 = models.Users(user_id=str(uuid.uuid4()), name="Test Taro")
    test_db.add(user1)
    test_db.flush()
    test_db.commit()
    response = client.delete("/users/" + user1.user_id + "/")
    assert response.status_code == 204


def test_read_scores(test_db):
    user1 = models.Users(user_id=str(uuid.uuid4()), name="Test Taro")
    user2 = models.Users(user_id=str(uuid.uuid4()), name="Test Jiro")
    test_db.add_all([user1, user2])
    test_db.flush()
    test_db.commit()

    score1 = models.Scores(user_id=user1.user_id, score_id=str(uuid.uuid4()), score=8000)
    score2 = models.Scores(user_id=user2.user_id, score_id=str(uuid.uuid4()), score=9900)
    score3 = models.Scores(user_id=user1.user_id, score_id=str(uuid.uuid4()), score=10000)
    score4 = models.Scores(user_id=user2.user_id, score_id=str(uuid.uuid4()), score=9500)
    score5 = models.Scores(user_id=user1.user_id, score_id=str(uuid.uuid4()), score=9300)
    score6 = models.Scores(user_id=user2.user_id, score_id=str(uuid.uuid4()), score=9800)
    test_db.add_all([score6, score5, score4, score3, score2, score1])
    test_db.flush()
    test_db.commit()

    response = client.get("/scores")

    assert response.status_code == 200
    assert response.json()[0]["score"] == 10000


def test_read_score(test_db):
    user1 = models.Users(user_id=str(uuid.uuid4()), name="Test Taro")
    test_db.add(user1)
    test_db.flush()
    test_db.commit()
    score1 = models.Scores(user_id=user1.user_id, score_id=str(uuid.uuid4()), score=100)
    test_db.add(score1)
    test_db.flush()
    test_db.commit()
    response = client.get("/scores/" + score1.score_id + "/")
    assert response.status_code == 200
    assert response.json()["score"] == 100


def test_create_score(test_db):
    user1 = models.Users(user_id=str(uuid.uuid4()), name="Test Taro")
    test_db.add(user1)
    test_db.flush()
    test_db.commit()
    response = client.post("/scores/", json={"score": 100, "user_id": user1.user_id})
    assert response.status_code == 201
    assert response.json()["score"] == 100


def test_update_score(test_db):
    user1 = models.Users(user_id=str(uuid.uuid4()), name="Test Taro")
    test_db.add(user1)
    test_db.flush()
    test_db.commit()
    score1 = models.Scores(user_id=user1.user_id, score_id=str(uuid.uuid4()), score=100)
    test_db.add(score1)
    test_db.flush()
    test_db.commit()
    response = client.put("/scores/" + score1.score_id + "/", json={"score": 300, "user_id": user1.user_id})
    assert response.status_code == 200
    assert response.json()["score"] == 300


def test_delete_score(test_db):
    user1 = models.Users(user_id=str(uuid.uuid4()), name="Test Taro")
    test_db.add(user1)
    test_db.flush()
    test_db.commit()
    score1 = models.Scores(user_id=user1.user_id, score_id=str(uuid.uuid4()), score=100)
    test_db.add(score1)
    test_db.flush()
    test_db.commit()
    response = client.delete("/scores/" + score1.score_id + "/")
    assert response.status_code == 204
