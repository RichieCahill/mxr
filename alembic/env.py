"""Alembic."""

from __future__ import annotations

import sys
import logging
from os import environ

from sqlalchemy import URL, create_engine

from alembic import context
from mxr.orm import MXRDB, Drinks  # noqa: F401

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config


target_metadata = MXRDB.metadata
logging.basicConfig(
    level="DEBUG",
    datefmt="%Y-%m-%dT%H:%M:%S%z",
    format="%(asctime)s %(levelname)s %(filename)s:%(lineno)d - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)


def run_migrations_offline(url: URL) -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online(url: URL) -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = create_engine(url)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_schemas=True,
            version_table_schema=MXRDB.schema_name,
        )

        with context.begin_transaction():
            context.run_migrations()


def get_url() -> URL:
    """Get the database URL from the environment."""
    return URL.create(
        drivername=environ["MXR_DATABASE_DRIVERNAME"],
        username=environ["MXR_DATABASE_USER"],
        password=environ["MXR_DATABASE_PASSWORD"],
        host=environ["MXR_DATABASE_HOST"],
        port=int(environ["MXR_DATABASE_PORT"]),
        database=environ["MXR_DATABASE_DATABASE"],
    )


url = get_url()


if context.is_offline_mode():
    run_migrations_offline(url)
else:
    run_migrations_online(url)
