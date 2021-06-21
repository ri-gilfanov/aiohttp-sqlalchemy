from aiohttp_sqlalchemy import __version__


def test_version() -> None:
    assert __version__ == '0.16.0'
