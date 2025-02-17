"""Test configuration."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from sqlalchemy import Engine, MetaData, create_engine
from sqlalchemy.orm import Session

from mxr.app import create_app
from mxr.orm import MXRDB

if TYPE_CHECKING:
    from flask import Flask
    from flask.testing import FlaskClient
    from pytest_mock import MockerFixture


def create_test_engine(schema_name: str, metadata: MetaData) -> Engine:
    """Create a test database."""
    test_engine = create_engine(
        "sqlite://",
        echo=False,
        execution_options={"schema_translate_map": {schema_name: None}},
    )

    with Session(test_engine) as session:
        metadata.create_all(test_engine)
        session.commit()

    return test_engine


@pytest.fixture
def app(mocker: MockerFixture) -> Flask:
    """Create an application for testing."""
    test_engine = create_test_engine(MXRDB.schema_name, MXRDB.metadata)

    mocker.patch("mxr.app.get_url", return_value="sqlite://")
    mocker.patch("mxr.app.create_engine", return_value=test_engine)

    return create_app()


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    """Create a flask test client."""
    return app.test_client()
