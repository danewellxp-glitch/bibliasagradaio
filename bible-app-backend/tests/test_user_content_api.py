"""Integration tests for User Content API (highlights, annotations, bookmarks)."""

import pytest
from fastapi.testclient import TestClient


def test_get_highlights_requires_auth(client: TestClient):
    """GET /api/v1/highlights returns 401 without token."""
    response = client.get("/api/v1/highlights")
    assert response.status_code == 401


def test_get_highlights_with_auth(auth_client: TestClient):
    """GET /api/v1/highlights returns 200 and list when authenticated."""
    response = auth_client.get("/api/v1/highlights")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_highlight_with_auth(auth_client: TestClient):
    """POST /api/v1/highlights creates highlight and returns 201."""
    response = auth_client.post(
        "/api/v1/highlights",
        json={
            "version_id": 1,
            "book_number": 1,
            "chapter": 1,
            "verse": 1,
            "color": "#ffff00",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["book_number"] == 1
    assert data["verse"] == 1
    assert data["color"] == "#ffff00"


def test_get_annotations_with_auth(auth_client: TestClient):
    """GET /api/v1/annotations returns 200 and list when authenticated."""
    response = auth_client.get("/api/v1/annotations")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_annotation_with_auth(auth_client: TestClient):
    """POST /api/v1/annotations creates annotation and returns 201."""
    response = auth_client.post(
        "/api/v1/annotations",
        json={
            "version_id": 1,
            "book_number": 1,
            "chapter": 1,
            "verse": 1,
            "note": "Test note from integration test",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["note"] == "Test note from integration test"


def test_get_bookmarks_with_auth(auth_client: TestClient):
    """GET /api/v1/bookmarks returns 200 and list when authenticated."""
    response = auth_client.get("/api/v1/bookmarks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_bookmark_with_auth(auth_client: TestClient):
    """POST /api/v1/bookmarks creates bookmark and returns 201."""
    response = auth_client.post(
        "/api/v1/bookmarks",
        json={
            "version_id": 1,
            "book_number": 1,
            "chapter": 1,
            "verse": 1,
            "title": "Test bookmark",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data.get("title") == "Test bookmark"


def test_delete_highlight_requires_auth(client: TestClient):
    """DELETE /api/v1/highlights/{id} returns 401 without token."""
    response = client.delete(
        "/api/v1/highlights/00000000-0000-0000-0000-000000000001"
    )
    assert response.status_code == 401
