import sqlalchemy as sa
from typing import TYPE_CHECKING

import aiohttp_sqlalchemy
from aiohttp_sqlalchemy import SA_DEFAULT_KEY, sa_session

if TYPE_CHECKING:
    from aiohttp.web import Application, Request
    from sqlalchemy.ext.asyncio import AsyncSession


async def test_db_init(middlewared_app: 'Application') -> None:
    metadata = sa.MetaData()
    await aiohttp_sqlalchemy.init_db(middlewared_app, metadata)


def test_sa_session(
    mocked_request: 'Request',
    orm_session: 'AsyncSession'
) -> None:
    mocked_request[SA_DEFAULT_KEY] = orm_session
    assert sa_session(mocked_request) is orm_session
