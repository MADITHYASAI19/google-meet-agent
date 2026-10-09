from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.exc import SQLAlchemyError
from backend.app.auth.models import User, RefreshToken
from backend.app.core.exceptions import EntityNotFoundException

class UserRepository:
    """
    Repository for User identity and profile management.
    """
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, email: str, hashed_password: str, full_name: str, role: str = "STUDENT") -> User:
        try:
            user = User(email=email, hashed_password=hashed_password, full_name=full_name, role=role)
            self.session.add(user)
            await self.session.flush()
            return user
        except SQLAlchemyError as e:
            raise Exception(f"Database error creating user: {str(e)}")

    async def get_by_email(self, email: str) -> User:
        result = await self.session.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        if not user:
            raise EntityNotFoundException(f"User with email {email} not found")
        return user

    async def get_by_id(self, user_id: int) -> User:
        result = await self.session.get(User, user_id)
        if not result:
            raise EntityNotFoundException(f"User with ID {user_id} not found")
        return result

    async def update(self, user_id: int, data: dict) -> User:
        user = await self.get_by_id(user_id)
        for key, value in data.items():
            setattr(user, key, value)
        await self.session.flush()
        return user

class RefreshTokenRepository:
    """
    Repository for managing refresh token lifecycles and revocation.
    """
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_id: int, token_hash: str, expires_at: Any) -> RefreshToken:
        try:
            token = RefreshToken(user_id=user_id, token_hash=token_hash, expires_at=expires_at)
            self.session.add(token)
            await self.session.flush()
            return token
        except SQLAlchemyError as e:
            raise Exception(f"Database error creating refresh token: {str(e)}")

    async def get_by_hash(self, token_hash: str) -> RefreshToken:
        result = await self.session.execute(select(RefreshToken).where(RefreshToken.token_hash == token_hash))
        token = result.scalar_one_or_none()
        if not token:
            raise EntityNotFoundException("Refresh token not found")
        return token

    async def revoke(self, token_hash: str):
        result = await self.session.execute(
            delete(RefreshToken).where(RefreshToken.token_hash == token_hash)
        )
        await self.session.flush()
