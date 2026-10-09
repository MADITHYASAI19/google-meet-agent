from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import StaticPool
from backend.app.config.settings import settings
import logging

logger = logging.getLogger("ai_lecture_assistant")

# Determine the async engine based on the DB URL
# SQLite requires aiosqlite for async support
# PostgreSQL requires asyncpg
db_url = settings.database.url

# For SQLite development, we ensure the driver is correct and use StaticPool for in-memory/shared access
if "sqlite" in db_url:
    # Ensure we use the async driver aiosqlite
    if not db_url.startswith("sqlite+aiosqlite"):
        db_url = db_url.replace("sqlite://", "sqlite+aiosqlite://")

    engine = create_async_engine(
        db_url,
        connect_args={"check_same_thread": False}, # Required for SQLite
        poolclass=StaticPool # Useful for dev/tests to keep connection alive
    )
else:
    # PostgreSQL / Other async drivers
    engine = create_async_engine(db_url, echo=settings.app.debug)

# Create an async session factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

async def init_db():
    """
    Initializes the database engine and verifies connectivity.
    """
    try:
        async with engine.begin() as conn:
            # For SQLite, we must enable foreign key constraints explicitly
            if "sqlite" in db_url:
                await conn.exec_driver_sql("PRAGMA foreign_keys = ON")
            logger.info("Database engine initialized and connectivity verified.")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise e
