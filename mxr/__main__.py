"""Main."""

from __future__ import annotations

import logging
import sys
from os import getenv


def main() -> None:
    """Main."""
    logging.basicConfig(
        level=getenv("LOG_LEVEL", "INFO"),
        datefmt="%Y-%m-%dT%H:%M:%S%z",
        format="%(asctime)s %(levelname)s %(filename)s:%(lineno)d - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )

    logging.info("Hello World")


if __name__ == "__main__":
    main()
