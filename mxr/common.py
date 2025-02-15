"""Common.

This module contains common code that is used throughout the project.
"""

from __future__ import annotations

from datetime import UTC, datetime


def utc_now() -> datetime:
    """Return the current UTC datetime."""
    return datetime.now(tz=UTC)
