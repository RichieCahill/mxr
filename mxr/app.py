"""App."""

from __future__ import annotations

import logging
import sys
from os import getenv

from flask import Flask
from sqlalchemy import create_engine

from mxr.common import get_url


def create_app() -> Flask:
    """Create the Flask app."""
    app = Flask(__name__)

    logging.basicConfig(
        level=getenv("LOG_LEVEL", "INFO"),
        datefmt="%Y-%m-%dT%H:%M:%S%z",
        format="%(asctime)s %(levelname)s %(filename)s:%(lineno)d - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )

    url = get_url("MXR")
    engine = create_engine(url)
    app.config["ENGINE"] = engine

    @app.route("/")
    def hello_world() -> str:
        """Hello world."""
        return "Hello World"

    return app
