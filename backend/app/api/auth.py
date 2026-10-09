from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Tuple, Any

from backend.app.db.session import get_db
from backend.app.auth.service import AuthService
from backend.app.auth.dependencies import get_current_user
from backend.app.auth.models import User
from backend.app.schemas.api_schemas import APIResponse
from backend.app.auth.exceptions import UserAlreadyExists

router = APIRouter()

@router.post("/register", response_model=APIResponse[dict], tags=["Auth"])
async def register(
    email: str = Body(...),
    password: str = Body(...),
    full_name: str = Body(...),
    db: AsyncSession = Depends(get_db)
):
    """Registers a new user account."""
    auth_service = AuthService(db)
    try:
        user = await auth_service.register(email=email, password=password, full_name=full_name)
        return APIResponse(
            data={"id": user.id, "email": user.email, "role": user.role},
            message="User registered successfully"
        )
    except UserAlreadyExists as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/login", response_model=APIResponse[dict], tags=["Auth"])
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """Authenticates user and returns JWT token pair."""
    auth_service = AuthService(db)
    try:
        # We pass mock request info for now (IP/UA)
        access_token, refresh_token = await auth_service.login(
            email=form_data.username,
            password=form_data.password,
            request_info={"ip": "unknown", "user_agent": "unknown"}
        )
        return APIResponse(
            data={"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"},
            message="Login successful"
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

@router.post("/refresh", response_model=APIResponse[dict], tags=["Auth"])
async def refresh(
    refresh_token: str = Body(...),
    db: AsyncSession = Depends(get_db)
):
    """Issues a new access token using a valid refresh token."""
    auth_service = AuthService(db)
    try:
        new_access, same_refresh = await auth_service.refresh_access_token(refresh_token)
        return APIResponse(
            data={"access_token": new_access, "refresh_token": same_refresh},
            message="Token refreshed successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

@router.post("/logout", tags=["Auth"])
async def logout(
    refresh_token: str = Body(...),
    db: AsyncSession = Depends(get_db)
):
    """Revokes the refresh token to end the session."""
    auth_service = AuthService(db)
    await auth_service.logout(refresh_token)
    return APIResponse(
        data={"status": "logged_out"},
        message="Successfully logged out"
    )

@router.get("/me", response_model=APIResponse[dict], tags=["Auth"])
async def get_me(
    user: User = Depends(get_current_user),
):
    """Retrieves the current authenticated user's profile."""
    return APIResponse(
        data={
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role,
            "is_active": user.is_active
        },
        message="User profile retrieved"
    )
