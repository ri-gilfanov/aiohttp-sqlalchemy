from sqlalchemy.sql.schema import MetaData
from aiohttp_sqlalchemy import DEFAULT_KEY, sa_init_db, sa_session
import sqlalchemy as sa


async def test_sa_db_init(middlewared_app):
    metadata = sa.MetaData()
    await sa_init_db(middlewared_app, metadata)


def test_sa_session(mocked_request, orm_session):
    mocked_request[DEFAULT_KEY] = orm_session
    assert sa_session(mocked_request) is orm_session
