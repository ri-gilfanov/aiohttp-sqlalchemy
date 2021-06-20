from aiohttp_sqlalchemy import __version__


def test_version():
    assert __version__ == '0.15.4'
