import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app


def test_home_page():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200


def test_health():
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_search_missing_query():
    client = app.test_client()
    response = client.get("/api/search")
    assert response.status_code == 400


def test_search_with_query():
    client = app.test_client()
    response = client.get("/api/search?q=chicken")
    assert response.status_code == 200
    data = response.get_json()
    assert "recipes" in data
