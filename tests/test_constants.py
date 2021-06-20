import aiohttp_sqlalchemy
from aiohttp_sqlalchemy import constants


def test_sa_default_key() -> None:
    assert aiohttp_sqlalchemy.SA_DEFAULT_KEY == 'sa_main'
    assert aiohttp_sqlalchemy.DEFAULT_KEY == 'sa_main'
    assert constants.SA_DEFAULT_KEY == 'sa_main'
    assert constants.DEFAULT_KEY == 'sa_main'
