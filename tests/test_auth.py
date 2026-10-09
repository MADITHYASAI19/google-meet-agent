import pytest
import asyncio
from httpx import AsyncClient
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.main import app
from backend.app.db.session import get_db
from backend.app.auth.service import AuthService
from backend.app.auth.jwt import jwt_handler
from backend.app.auth.models import User
from backend.app.auth.dependencies import get_current_user

# Mock DB session for dependency override
async def override_get_db():
    # This should return a test database session
    # For the purpose of this template, we assume a test_db is configured
    from backend.app.db.session import SessionLocal
    async with SessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
async def test_user():
    """Creates a test user in the database."""
    from backend.app.db.session import SessionLocal
    async with SessionLocal() as db:
        auth_service = AuthService(db)
        user = await auth_service.register(
            email="test@example.com",
            password="Password123!",
            full_name="Test User",
            role="STUDENT"
        )
        return user

@pytest.fixture
async def auth_token(test_user):
    """Generates a valid JWT for the test user."""
    return jwt_handler.create_access_token({
        "sub": str(test_user.id),
        "email": test_user.email,
        "role": test_user.role
    })

@pytest.fixture
async def authenticated_client(auth_token):
    """Provides an AsyncClient with authorization headers."""
    client = AsyncClient(app=app, base_url="http://test")
    client.headers.update({"Authorization": f"Bearer {auth_token}"})
    return client

@pytest.mark.asyncio
async def test_login_success(test_user):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/api/auth/login",
            data={"username": test_user.email, "password": "Password123!"}
        )
        assert response.status_code == 200
        assert "access_token" in response.json()["data"]

@pytest.mark.asyncio
async def test_protected_endpoint_no_token():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/meetings/123")
        assert response.status_code == 401

@pytest.mark.asyncio
async def test_protected_endpoint_with_token(authenticated_client):
    response = await authenticated_client.get("/api/meetings/123")
    # Should not be 401 now
    assert response.status_code != 401

@pytest.mark.asyncio
async def test_forbidden_role(test_user):
    # Set user to student and try to access faculty endpoint
    token = jwt_handler.create_access_token({"sub": str(test_user.id), "role": "STUDENT"})
    async with AsyncClient(app=app, base_url="http://test") as ac:
        ac.headers.update({"Authorization": f"Bearer {token}"})
        # Attempt to join meeting (RequireFaculty)
        response = await ac.post("/api/meetings/join", json={"url": "http://meet.google.com/abc"})
        assert response.status_code == 403

@pytest.mark.asyncio
async def test_websocket_auth_success(auth_token):
    with TestClient(app) as client:
        with client.websocket_connect(f"/ws?token={auth_token}") as websocket:
            # Connection should be accepted
            assert websocket.get_code() is None # No close code means still open

@pytest.mark.asyncio
async def test_websocket_auth_fail():
    with TestClient(app) as client:
        with client.websocket_connect("/ws?token=invalid_token") as websocket:
            # Connection should be closed with 1008
            assert websocket.get_code() == 1008
