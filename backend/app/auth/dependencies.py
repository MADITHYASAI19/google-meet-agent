from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from backend.app.db.session import get_db
from backend.app.auth.jwt import jwt_handler
from backend.app.auth.models import User
from backend.app.auth.exceptions import AuthenticationFailed, AuthorizationDenied, InvalidToken, ExpiredToken
from backend.app.repositories.auth_repositories import UserRepository
from backend.app.config.logging_config import setup_logging

logger = setup_logging()

# Token extraction from Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Validates the JWT and retrieves the current authenticated user.
    """
    try:
        payload = jwt_handler.decode_token(token)
        user_id = payload.get("sub")
        if not user_id:
            raise AuthenticationFailed("Token payload missing user identifier")

        user_repo = UserRepository(db)
        user = await user_repo.get_by_id(int(user_id))

        if not user.is_active:
            from backend.app.auth.exceptions import InactiveUser
            raise InactiveUser()

        return user
    except (InvalidToken, ExpiredToken) as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except Exception as e:
        logger.error(f"Auth dependency error: {e}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

class RoleChecker:
    """
    Role-Based Access Control dependency.
    """
    def __init__(self, allowed_roles: list[str]):
        self.allowed_roles = allowed_roles

    async def __call__(self, user: User = Depends(get_current_user)):
        if user.role not in self.allowed_roles:
            logger.warning(f"User {user.email} with role {user.role} denied access. Required: {self.allowed_roles}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource"
            )
        return user

# Pre-defined Role Dependencies
RequireAuthenticated = Depends(get_current_user)
RequireAdmin = Depends(RoleChecker(["ADMIN"]))
RequireFaculty = Depends(RoleChecker(["ADMIN", "FACULTY"]))
RequireStudent = Depends(RoleChecker(["ADMIN", "FACULTY", "STUDENT"]))
