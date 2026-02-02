"""Integration tests for Quiz API endpoints."""

import pytest
from fastapi.testclient import TestClient


def test_quiz_next_question_requires_auth(client: TestClient):
    """GET /api/v1/quiz/next-question returns 401 without token."""
    response = client.get("/api/v1/quiz/next-question")
    assert response.status_code == 401


def test_quiz_next_question_with_auth(auth_client: TestClient):
    """GET /api/v1/quiz/next-question returns 200 or 404 when authenticated."""
    response = auth_client.get("/api/v1/quiz/next-question")
    assert response.status_code in (200, 404)
    if response.status_code == 200:
        data = response.json()
        assert "id" in data
        assert "question_text" in data
        assert "options" in data
        assert isinstance(data["options"], list)


def test_quiz_stats_with_auth(auth_client: TestClient):
    """GET /api/v1/quiz/stats returns 200 when authenticated."""
    response = auth_client.get("/api/v1/quiz/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_xp" in data
    assert "current_level" in data
    assert "current_streak" in data
    assert "total_questions_answered" in data


def test_quiz_leaderboard_no_auth_required(client: TestClient):
    """GET /api/v1/quiz/leaderboard is public."""
    response = client.get("/api/v1/quiz/leaderboard")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_quiz_submit_answer_requires_auth(client: TestClient):
    """POST /api/v1/quiz/answer returns 401 without token."""
    response = client.post(
        "/api/v1/quiz/answer",
        json={"question_id": 1, "answer": "A", "time_taken_seconds": 10},
    )
    assert response.status_code == 401


def test_quiz_submit_answer_with_auth(auth_client: TestClient):
    """POST /api/v1/quiz/answer returns 200/404/409 when authenticated."""
    response = auth_client.post(
        "/api/v1/quiz/answer",
        json={"question_id": 99999, "answer": "X", "time_taken_seconds": 5},
    )
    assert response.status_code in (200, 404, 409)
    if response.status_code == 200:
        data = response.json()
        assert "is_correct" in data
        assert "xp_earned" in data
        assert "new_total_xp" in data
