from app.core.security import create_jwt_token, verify_jwt_token


def test_create_and_verify_jwt():
    token = create_jwt_token("test-user-id")
    payload = verify_jwt_token(token)
    assert payload["sub"] == "test-user-id"


def test_health_still_works(client):
    response = client.get("/health")
    assert response.status_code == 200
