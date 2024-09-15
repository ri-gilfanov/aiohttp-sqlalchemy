from pathlib import Path

import tomli

from aiohttp_sqlalchemy import __version__


def test_version() -> None:
    with Path("./pyproject.toml").open("rb") as f:
        pyproject = tomli.load(f)
        version = pyproject["tool"]["poetry"]["version"]
        assert __version__ == version
