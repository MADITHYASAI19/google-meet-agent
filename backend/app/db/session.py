from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.db.database import AsyncSessionLocal

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency that provides an asynchronous database session.
    The session is automatically closed after the request is completed.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

class DBContextManager:
    """
    A context manager for managing database sessions outside of FastAPI requests
    (e.g., in background tasks or event listeners).
    """
    async def __aenter__(self):
        self.session = AsyncSessionLocal()
        return self.session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()
