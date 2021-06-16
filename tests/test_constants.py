import aiohttp_sqlalchemy
from aiohttp_sqlalchemy import constants


def test_default_key():
    assert aiohttp_sqlalchemy.DEFAULT_KEY == 'sa_main'
    assert constants.DEFAULT_KEY == 'sa_main'


def test_sa_default_key():
    assert constants.SA_DEFAULT_KEY == 'sa_main'
