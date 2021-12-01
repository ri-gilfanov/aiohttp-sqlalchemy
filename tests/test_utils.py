import pytest
import sqlalchemy as sa
from aiohttp.web import Application, Request
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker

import aiohttp_sqlalchemy as ahsa


async def test_db_init(middlewared_app: Application) -> None:
    metadata = sa.MetaData()
    await ahsa.init_db(middlewared_app, metadata)


async def test_get_engine(middlewared_app: Application) -> None:
    engine = await ahsa.get_engine(middlewared_app)
    assert isinstance(engine, AsyncEngine)


def test_get_session(mocked_request: Request, session: AsyncSession) -> None:
    mocked_request[ahsa.DEFAULT_KEY] = session
    assert ahsa.get_session(mocked_request) is session

    with pytest.raises(TypeError):
        ahsa.get_session(None)  # type: ignore

    with pytest.raises(TypeError):
        ahsa.get_session(mocked_request, 'wrong key')


def test_get_session_factory(
    mocked_request: Request,
    middlewared_app: Application,
    session_factory: sessionmaker,
) -> None:
    assert ahsa.get_session_factory(mocked_request) is session_factory
    assert ahsa.get_session_factory(middlewared_app) is session_factory
    with pytest.raises(TypeError):
        ahsa.get_session_factory(None)  # type: ignore
