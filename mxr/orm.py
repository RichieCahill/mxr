"""ORM."""

from __future__ import annotations

# I think we need this hear but I'm not sure
# TODO(Richie): test once we have a working database
from datetime import datetime  # noqa: TC003
from os import getenv

from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import AbstractConcreteBase
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, object_session

from mxr.common import utc_now


def get_object_session(instance: object) -> Session:
    """Return the session bound to the given object.

    Args:
        instance: The object to get the session for.

    Returns:
        The session bound to the object.

    Raises:
        RuntimeError: If the object is not bound to a session.
    """
    if session := object_session(instance):
        return session
    error = f"Object {instance} is not bound to a session"
    raise RuntimeError(error)


class MXRDB(DeclarativeBase):
    """Base class for all models."""

    schema_name = getenv("MXR_SCHEMA", "mxr")

    metadata = MetaData(schema=schema_name)


class IdTimestampColumns:
    """Mixin for models that have an id and timestamp columns."""

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(onupdate=utc_now, default=utc_now)


class TableBase(AbstractConcreteBase, MXRDB, IdTimestampColumns):
    """Base class for all tables."""


class Drinks(TableBase):
    """Table for drinks."""

    __tablename__ = "drinks"

    # fmt: off

    name:           Mapped[str]
    garnish:        Mapped[str | None]
    ingredients:    Mapped[str]
    preparation:    Mapped[str]

    # fmt: on
