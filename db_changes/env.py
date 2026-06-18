import os
from logging.config import fileConfig

from alembic import context
from archipy.models.entities import BaseEntity
from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool

# Load environment variables
load_dotenv()

# this is the Alembic Config object
config = context.config

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Build database URL from environment variables
DB_USER = os.getenv("POSTGRES_SQLALCHEMY__USERNAME", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_SQLALCHEMY__PASSWORD", "postgres")
DB_HOST = os.getenv("POSTGRES_SQLALCHEMY__HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_SQLALCHEMY__PORT", "5432")
DB_NAME = os.getenv("POSTGRES_SQLALCHEMY__DATABASE", "attendance")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Import your Base metadata here when you have models
# For now, we'll set target_metadata to None
# from src.models.entities import Base
# target_metadata = Base.metadata
from src.models.entities import *

target_metadata = BaseEntity.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
