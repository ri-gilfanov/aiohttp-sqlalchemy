import aiohttp_sqlalchemy
from aiohttp_sqlalchemy import SA_DEFAULT_KEY, sa_session
import sqlalchemy as sa


async def test_db_init(middlewared_app):
    metadata = sa.MetaData()
    await aiohttp_sqlalchemy.init_db(middlewared_app, metadata)


def test_sa_session(mocked_request, orm_session):
    mocked_request[SA_DEFAULT_KEY] = orm_session
    assert sa_session(mocked_request) is orm_session
