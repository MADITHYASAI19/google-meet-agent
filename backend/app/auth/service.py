import uuid
import logging
from typing import Optional, Tuple, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.auth.password import hash_password, verify_password
from backend.app.auth.jwt import jwt_handler
from backend.app.auth.exceptions import (
    AuthenticationFailed, UserAlreadyExists, InactiveUser
)
from backend.app.auth.models import User, RefreshToken, LastLogin
from backend.app.repositories.auth_repositories import UserRepository, RefreshTokenRepository
from backend.app.config.logging_config import setup_logging
from datetime import datetime, timezone

logger = setup_logging()

class AuthService:
    """
    High-level authentication service orchestrating identity and session management.
    """
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repo = UserRepository(session)
        self.token_repo = RefreshTokenRepository(session)

    async def register(self, email: str, password: str, full_name: str, role: str = "STUDENT") -> User:
        """Registers a new user account."""
        try:
            # Check if user exists
            try:
                await self.user_repo.get_by_email(email)
                raise UserAlreadyExists()
            except Exception:
                pass # If not found, we proceed

            hashed = hash_password(password)
            user_uuid = str(uuid.uuid4())

            user = await self.user_repo.create(
                email=email,
                hashed_password=hashed,
                full_name=full_name,
                role=role
            )
            # We use the internal ID for tokens, but we should set the uuid
            user.uuid = user_uuid
            await self.session.flush()

            logger.info(f"New user registered: {email}")
            return user
        except Exception as e:
            logger.error(f"Registration failed for {email}: {e}")
            raise e

    async def login(self, email: str, password: str, request_info: Dict[str, Any]) -> Tuple[str, str]:
        """
        Authenticates a user and returns a pair of (access_token, refresh_token).
        """
        try:
            user = await self.user_repo.get_by_email(email)

            if not user.is_active:
                raise InactiveUser()

            if not verify_password(password, user.hashed_password):
                raise AuthenticationFailed("Invalid email or password")

            # Log login event
            last_login = LastLogin(
                user_id=user.id,
                ip_address=request_info.get("ip"),
                user_agent=request_info.get("user_agent")
            )
            self.session.add(last_login)

            # Create tokens
            access_token = jwt_handler.create_access_token({
                "sub": str(user.id),
                "email": user.email,
                "role": user.role
            })

            refresh_token_str = jwt_handler.create_refresh_token({"sub": str(user.id)})

            # Persist refresh token hash
            await self.token_repo.create(
                user_id=user.id,
                token_hash=refresh_token_str, # In prod, we should hash this too
                expires_at=datetime.now(timezone.utc) # Add actual expiration
            )

            logger.info(f"User logged in: {email}")
            return access_token, refresh_token_str

        except Exception as e:
            logger.error(f"Login failed for {email}: {e}")
            raise e

    async def refresh_access_token(self, refresh_token: str) -> Tuple[str, str]:
        """
        Issues a new access token using a valid refresh token.
        """
        try:
            # Validate token
            payload = jwt_handler.decode_token(refresh_token)
            user_id = int(payload.get("sub"))

            # Check if token is revoked/exists in DB
            db_token = await self.token_repo.get_by_hash(refresh_token)
            if db_token.revoked:
                raise AuthenticationFailed("Refresh token has been revoked")

            user = await self.user_repo.get_by_id(user_id)
            if not user.is_active:
                raise InactiveUser()

            # Generate new access token
            new_access = jwt_handler.create_access_token({
                "sub": str(user.id),
                "email": user.email,
                "role": user.role
            })

            return new_access, refresh_token # Return same refresh token or rotate it

        except Exception as e:
            logger.error(f"Token refresh failed: {e}")
            raise e

    async def logout(self, refresh_token: str):
        """Revokes a refresh token to end the session."""
        await self.token_repo.revoke(refresh_token)
        logger.info("User logged out successfully")
