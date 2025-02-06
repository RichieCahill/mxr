"""Test code compliance."""

from __future__ import annotations

import logging
from re import match
from subprocess import PIPE, Popen


def bash_wrapper(command: str) -> tuple[str, int]:
    """Execute a bash command and capture the output.

    Args:
        command (str): The bash command to be executed.

    Returns:
        Tuple[str, int]: A tuple containing the output of the command (stdout) as a string,
        the error output (stderr) as a string (optional), and the return code as an integer.
    """
    # This is a acceptable risk
    process = Popen(command.split(), stdout=PIPE, stderr=PIPE)  # noqa: S603
    output, error = process.communicate()
    if error:
        logging.error(f"{error=}")

    return output.decode(), process.returncode


def test_ruff_check() -> None:
    """Test ruff check."""
    stdout, returncode = bash_wrapper("poetry run ruff check .")
    assert stdout == "All checks passed!\n"
    assert returncode == 0


def test_ruff_format() -> None:
    """Test ruff format."""
    stdout, returncode = bash_wrapper("poetry run ruff format --check .")
    test = stdout.strip()
    assert match(r"[\d]* files already formatted", test)
    assert returncode == 0


def test_mypy_check() -> None:
    """Test mypy check."""
    stdout, returncode = bash_wrapper("poetry run mypy .")
    test = stdout.strip()
    assert match(r"Success: no issues found in [\d]* source files", test)
    assert returncode == 0
