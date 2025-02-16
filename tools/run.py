from __future__ import annotations

import multiprocessing
from typing import Any

from gunicorn.app.wsgiapp import WSGIApplication


class StandaloneApplication(WSGIApplication):
    """Standalone WSGI application class.

    This class is used to run the application in a standalone mode.
    """

    def __init__(self, app_uri: str, options: dict[str, Any] | None = None) -> None:
        """Initialize the application.

        Args:
            app_uri (str): The URI of the application.
            options (dict[str, Any], optional): The options for the application. Defaults to None.
        """
        self.options = options or {}
        self.app_uri = app_uri
        super().__init__()

    def load_config(self) -> None:
        """Load the configuration for the application."""
        if self.cfg is None:
            error = "Configuration not loaded."
            raise RuntimeError(error)

        config = {key: value for key, value in self.options.items() if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)


def main() -> None:
    """Run the application."""
    options = {
        "bind": "127.0.0.1:3000",
        "workers": (multiprocessing.cpu_count() * 2) + 1,
        "worker_class": "uvicorn.workers.UvicornWorker",
    }
    StandaloneApplication("mxr.app:create_app()", options).run()
