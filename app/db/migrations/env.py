import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

from logging.config import fileConfig
import asyncio

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine

from alembic import context

from app.db.base import Base
from app.core.config import get_settings
import app.db.models  # 👈 VERY IMPORTANT

# Alembic Config
config = context.config

# Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata
target_metadata = Base.metadata


# 🔥 Load settings
settings = get_settings()

DATABASE_URL = (
    f"mysql+aiomysql://{settings.DB_USER}:{settings.DB_PASSWORD}"
    f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)


# -----------------------------
# OFFLINE MODE
# -----------------------------
def run_migrations_offline() -> None:
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


# -----------------------------
# ONLINE MODE (ASYNC)
# -----------------------------
def run_migrations_online() -> None:
    connectable = create_async_engine(
        DATABASE_URL,
        poolclass=pool.NullPool,
    )

    async def do_run_migrations():
        async with connectable.connect() as connection:
            await connection.run_sync(run_migrations)

    def run_migrations(connection):
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()

    asyncio.run(do_run_migrations())


# -----------------------------
# ENTRY
# -----------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()