from typing import TYPE_CHECKING

import sqlalchemy as sa
from aiohttp.web import Application

import aiohttp_sqlalchemy
from aiohttp_sqlalchemy import SA_DEFAULT_KEY, sa_session, sa_session_factory

if TYPE_CHECKING:
    from aiohttp.web import Request
    from sqlalchemy.ext.asyncio import AsyncSession

    from aiohttp_sqlalchemy.typedefs import TSessionFactory


async def test_db_init(middlewared_app: "Application") -> None:
    metadata = sa.MetaData()
    await aiohttp_sqlalchemy.init_db(middlewared_app, metadata)


def test_sa_session(mocked_request: "Request", orm_session: "AsyncSession") -> None:
    mocked_request[SA_DEFAULT_KEY] = orm_session
    assert sa_session(mocked_request) is orm_session


def test_sa_session_factory(
    mocked_request: "Request",
    middlewared_app: "Application",
    orm_session_factory: "TSessionFactory",
) -> None:
    assert sa_session_factory(mocked_request) is orm_session_factory
    assert sa_session_factory(middlewared_app) is orm_session_factory
