from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool, create_engine
from alembic import context

# Import project settings and base
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app.config.settings import settings
from backend.app.db.base import Base

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# This is the critical part: we must import all models to ensure they are registered with Base.metadata
from backend.app.db import models

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = settings.database.url
    # Alembic offline mode doesn't support async drivers directly,
    # so we strip the +aiosqlite/asyncpg for the offline URL if present
    offline_url = url.replace("+aiosqlite", "").replace("+asyncpg", "")

    context.configure(
        url=offline_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    # We use synchronous engine for Alembic migrations as it's the standard for Alembic
    # We strip async drivers for the migration connection
    sync_url = settings.database.url.replace("+aiosqlite", "").replace("+asyncpg", "")

    connectable = create_engine(sync_url, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
