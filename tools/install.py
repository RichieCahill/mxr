from __future__ import annotations

from subprocess import run


def main() -> None:
    """Run the application."""
    run("git clone https://github.com/RichieCahill/mxr.git", check=True)

    run("poetry install", check=True)


if __name__ == "__main__":
    main()
