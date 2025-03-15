"""ORM."""

from __future__ import annotations

# This is required because datetime is required during runtime fro sqlalchemy
from datetime import datetime  # noqa: TC003
from os import getenv

from sqlalchemy import ForeignKey, Index, MetaData, String, UniqueConstraint
from sqlalchemy.ext.associationproxy import AssociationProxy, association_proxy
from sqlalchemy.ext.declarative import AbstractConcreteBase
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, object_session, relationship
from sqlalchemy.orm.collections import attribute_keyed_dict

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


class Drink(TableBase):
    """Table for drinks."""

    __tablename__ = "drinks"

    # fmt: off

    name:            Mapped[str]
    preparation:     Mapped[str]
    alcohol_content: Mapped[float | None]
    data_source:     Mapped[str | None]
    drink_type:      Mapped[str | None]
    garnish:         Mapped[str | None]
    glass:           Mapped[str | None]

    # fmt: on

    drinks_ingredients_associations: Mapped[dict[Ingredient, DrinkIngredientAssociation]] = relationship(
        "DrinkIngredientAssociation",
        back_populates="drink",
        collection_class=attribute_keyed_dict("ingredient"),
        cascade="all, delete-orphan",
    )

    ingredients: AssociationProxy[dict[Ingredient, str]] = association_proxy(
        "drinks_ingredients_associations",
        "measurement",
        creator=lambda ingredient_obj, measurement_str: DrinkIngredientAssociation(
            ingredient=ingredient_obj,
            measurement=measurement_str,
        ),
    )


class Ingredient(TableBase):
    """Table for ingredients."""

    __tablename__ = "ingredients"
    __table_args__ = (UniqueConstraint("name"),)

    # fmt: off
    name:              Mapped[str]
    alcohol_content:   Mapped[float | None]
    category:          Mapped[str | None]

    # fmt: on


class DrinkIngredientAssociation(TableBase):
    """DrinkIngredientAssociation."""

    __tablename__ = "drink_ingredient_associations"
    __table_args__ = (
        UniqueConstraint("drinks_id", "ingredients_id"),
        Index("drinks_id", "drinks_id"),
        Index("ingredients_id", "ingredients_id"),
    )

    # fmt: off

    drinks_id:      Mapped[int] = mapped_column(ForeignKey("drinks.id"))
    ingredients_id: Mapped[int] = mapped_column(ForeignKey("ingredients.id"))
    measurement:    Mapped[str] = mapped_column(String(50))

    drink:          Mapped[Drink] = relationship(back_populates="drinks_ingredients_associations")

    ingredient:     Mapped[Ingredient] = relationship()

    # fmt: off
