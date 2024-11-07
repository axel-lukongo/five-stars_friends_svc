import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from main import app, Base

SQLALCHEMY_DATABASE_URL = "postgresql://friend_db:friendpsw@localhost:5432/postgre_auth"  # Modifier selon votre config

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="module")
def db():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()

def test_add_friend(client, db):
    response = client.post(
        "/api/v1/create_friends/",
        json={"user_id": 1, "friend_id": 2}
    )
    assert response.status_code == 200
    assert response.json()["user_id"] == 1
    assert response.json()["friend_id"] == 2

def test_send_friend_request(client, db):
    response = client.post(
        "/api/v1/send_friend_requests/",
        json={"sender_id": 1, "receiver_id": 2}
    )
    assert response.status_code == 200
    assert response.json()["sender_id"] == 1
    assert response.json()["receiver_id"] == 2

def test_get_user_friends(client, db):
    response = client.get("/api/v1/get_friends/1")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_user_friend_requests(client, db):
    response = client.get("/api/v1/get_friend_requests/1")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_friend_request(client, db):
    response = client.put("/api/v1/update_friend_requests/1?status=accepted")
    assert response.status_code == 200
    assert response.json()["status"] == "accepted"

def test_delete_friend(client, db):
    response = client.delete("/api/v1/delete/1")
    assert response.status_code == 200

    response = client.delete("/api/v1/delete/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Friend not found"
