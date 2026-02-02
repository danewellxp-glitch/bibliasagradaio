import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.core.security import get_current_user
from app.main import app
from app.models.user import User


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def test_user(db: Session) -> User:
    """Create or get a test user for authenticated integration tests."""
    from sqlalchemy import select
    stmt = select(User).where(User.firebase_uid == "test-integration-fixture")
    existing = db.execute(stmt).scalars().first()
    if existing:
        return existing
    user = User(
        id=uuid.uuid4(),
        firebase_uid="test-integration-fixture",
        email="test@integration.test",
        display_name="Test User",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def auth_client(client: TestClient, test_user: User):
    """Client with get_current_user overridden to return test_user."""
    async def override_get_current_user():
        return test_user

    app.dependency_overrides[get_current_user] = override_get_current_user
    try:
        yield client
    finally:
        app.dependency_overrides.pop(get_current_user, None)
