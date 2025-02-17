"""Common.

This module contains common code that is used throughout the project.
"""

from __future__ import annotations

from datetime import UTC, datetime
from os import environ

from sqlalchemy import URL


def utc_now() -> datetime:
    """Return the current UTC datetime."""
    return datetime.now(tz=UTC)


def get_url(name: str) -> URL:
    """Get the database URL from the environment."""
    name = name.upper()
    return URL.create(
        drivername=environ[f"{name}_DATABASE_DRIVERNAME"],
        username=environ[f"{name}_DATABASE_USER"],
        password=environ[f"{name}_DATABASE_PASSWORD"],
        host=environ[f"{name}_DATABASE_HOST"],
        port=int(environ[f"{name}_DATABASE_PORT"]),
        database=environ[f"{name}_DATABASE_DATABASE"],
    )
