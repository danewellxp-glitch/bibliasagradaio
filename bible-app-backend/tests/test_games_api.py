"""Tests for the multiplayer games API."""


def test_create_room(auth_client):
    res = auth_client.post(
        "/api/v1/games/room/create",
        json={
            "game_type": "quiz",
            "difficulty": "beginner",
            "max_players": 5,
            "total_questions": 10,
        },
    )
    assert res.status_code == 200
    data = res.json()
    assert "room_code" in data
    assert len(data["room_code"]) == 6
    assert data["game_type"] == "quiz"
    assert data["difficulty"] == "beginner"
    assert data["max_players"] == 5


def test_get_room_status(auth_client):
    # Create a room first
    create_res = auth_client.post(
        "/api/v1/games/room/create",
        json={"game_type": "quiz", "difficulty": "beginner"},
    )
    code = create_res.json()["room_code"]

    # Get status (no auth needed)
    res = auth_client.get(f"/api/v1/games/room/{code}/status")
    assert res.status_code == 200
    data = res.json()
    assert data["room_code"] == code
    assert data["status"] == "waiting"
    assert len(data["participants"]) == 1  # creator auto-joined


def test_room_not_found(auth_client):
    res = auth_client.get("/api/v1/games/room/XXXXXX/status")
    assert res.status_code == 404


def test_start_game(auth_client):
    # Create room
    create_res = auth_client.post(
        "/api/v1/games/room/create",
        json={"game_type": "quiz", "difficulty": "beginner", "total_questions": 5},
    )
    code = create_res.json()["room_code"]

    # Can't start with only 1 player (but endpoint allows it if creator)
    start_res = auth_client.post(f"/api/v1/games/room/{code}/start")
    assert start_res.status_code == 200

    # Check status is now playing
    status_res = auth_client.get(f"/api/v1/games/room/{code}/status")
    assert status_res.json()["status"] == "playing"


def test_verse_of_the_day(auth_client):
    res = auth_client.get("/api/v1/bible/verse-of-the-day")
    # May return 404 if no Bible data is loaded, but endpoint should exist
    assert res.status_code in (200, 404)


def test_premium_status(auth_client):
    res = auth_client.get("/api/v1/premium/status")
    assert res.status_code == 200
    data = res.json()
    assert data["is_premium"] is False
    assert data["plan"] == "free"
    assert data["ai_daily_limit"] == 3
