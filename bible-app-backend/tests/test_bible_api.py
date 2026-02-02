"""Integration tests for Bible API endpoints."""

import pytest
from fastapi.testclient import TestClient


def test_get_versions(client: TestClient):
    """GET /api/v1/bible/versions returns list of versions."""
    response = client.get("/api/v1/bible/versions")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for item in data:
        assert "id" in item or "code" in item or "name" in item


def test_get_chapter_not_found(client: TestClient):
    """GET /api/v1/bible/{version}/{book}/{chapter} returns 404 when chapter has no data."""
    response = client.get("/api/v1/bible/ARA/1/999")
    assert response.status_code == 404


def test_get_chapter_invalid_book(client: TestClient):
    """GET /api/v1/bible with book=0 or book>66 returns 422."""
    response = client.get("/api/v1/bible/ARA/0/1")
    assert response.status_code == 422
    response = client.get("/api/v1/bible/ARA/67/1")
    assert response.status_code == 422


def test_get_chapter_valid(client: TestClient):
    """GET /api/v1/bible/{version}/{book}/{chapter} returns chapter when data exists."""
    response = client.get("/api/v1/bible/ARA/1/1")
    if response.status_code == 200:
        data = response.json()
        assert "book_number" in data
        assert data["book_number"] == 1
        assert data["chapter"] == 1
        assert "verses" in data
        assert isinstance(data["verses"], list)
    else:
        assert response.status_code == 404


def test_get_verse_valid(client: TestClient):
    """GET /api/v1/bible/{version}/{book}/{chapter}/{verse} returns verse when exists."""
    response = client.get("/api/v1/bible/ARA/1/1/1")
    if response.status_code == 200:
        data = response.json()
        assert "book_number" in data
        assert data["verse"] == 1
        assert "text" in data
    else:
        assert response.status_code == 404


def test_get_verse_invalid_verse_number(client: TestClient):
    """GET /api/v1/bible with verse > 176 returns 422."""
    response = client.get("/api/v1/bible/ARA/1/1/200")
    assert response.status_code == 422


def test_search_bible(client: TestClient):
    """GET /api/v1/bible/{version}/search?q=... returns search results."""
    response = client.get("/api/v1/bible/ARA/search", params={"q": "Deus"})
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "results" in data
    assert isinstance(data["results"], list)
