import pytest
import sqlalchemy as sa
from aiohttp.web import Application, Request
from sqlalchemy.ext.asyncio import AsyncSession

import aiohttp_sqlalchemy
from aiohttp_sqlalchemy import SA_DEFAULT_KEY, sa_session, sa_session_factory
from aiohttp_sqlalchemy.typedefs import TSessionFactory


async def test_db_init(middlewared_app: Application) -> None:
    metadata = sa.MetaData()
    await aiohttp_sqlalchemy.init_db(middlewared_app, metadata)


def test_sa_session(mocked_request: Request, session: AsyncSession) -> None:
    mocked_request[SA_DEFAULT_KEY] = session
    assert sa_session(mocked_request) is session
    with pytest.raises(TypeError):
        sa_session(None)  # type: ignore
    with pytest.raises(TypeError):
        sa_session(mocked_request, 'wrong key')


def test_sa_session_factory(
    mocked_request: Request,
    middlewared_app: Application,
    session_factory: TSessionFactory,
) -> None:
    assert sa_session_factory(mocked_request) is session_factory
    assert sa_session_factory(middlewared_app) is session_factory
