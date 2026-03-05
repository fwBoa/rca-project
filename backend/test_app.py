import pytest
from unittest.mock import patch, MagicMock
from app import app
from datetime import datetime

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        with app.app_context():
            yield client

@patch("app.psycopg2.connect")
@patch("app.redis.from_url")
def test_health(mock_redis, mock_pg, client):
    rv = client.get("/health")
    assert rv.status_code == 200
    assert "status" in rv.get_json()
    assert rv.get_json()["status"] == "ok"

@patch("app.psycopg2.connect")
@patch("app.redis.from_url")
def test_list_tasks(mock_redis, mock_pg, client):
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_pg.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cur
    
    # Mock some db return value
    mock_cur.fetchall.return_value = [
        {"id": 1, "title": "Test Task", "description": "", "is_active": True, "created_at": datetime.now(), "updated_at": datetime.now()}
    ]
    
    rv = client.get("/api/tasks")
    assert rv.status_code == 200
    data = rv.get_json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["title"] == "Test Task"

@patch("app.psycopg2.connect")
@patch("app.redis.from_url")
def test_create_task(mock_redis, mock_pg, client):
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_pg.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cur
    
    mock_cur.fetchone.return_value = {
        "id": 2, "title": "New Task", "description": "Desc", "is_active": True, "created_at": datetime.now(), "updated_at": datetime.now()
    }
    
    rv = client.post("/api/tasks", json={"title": "New Task"})
    assert rv.status_code == 201
    assert rv.get_json()["title"] == "New Task"

@patch("app.psycopg2.connect")
@patch("app.redis.from_url")
def test_create_task_invalid(mock_redis, mock_pg, client):
    rv = client.post("/api/tasks", json={"description": "Missing title"})
    assert rv.status_code == 400
