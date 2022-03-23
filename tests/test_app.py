import uuid

from fastapi.testclient import TestClient

from app.main import app
from app import models

client = TestClient(app)


def test_read_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"health": "true"}


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

    score1 = models.Scores(user_id=user1.user_id, score_id=str(uuid.uuid4()), score=100)
    score2 = models.Scores(user_id=user2.user_id, score_id=str(uuid.uuid4()), score=200)
    test_db.add_all([score1, score2])
    test_db.flush()
    test_db.commit()

    response = client.get("/scores")

    assert response.status_code == 200
    assert response.json()[0]["score"] == 100 or 200


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
