from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pytest
import sqlalchemy as sa
from aiohttp import web
from aiohttp.hdrs import METH_GET
from aiohttp.test_utils import make_mocked_request
from aiohttp.web import Request, Response
from sqlalchemy import orm
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

import aiohttp_sqlalchemy
from aiohttp_sqlalchemy import SA_DEFAULT_KEY, sa_bind, sa_middleware

if TYPE_CHECKING:  # pragma: no cover
    from aiohttp.web_app import Application

    from aiohttp_sqlalchemy.typedefs import THandler


pytest_plugins = "aiohttp.pytest_plugin"


@pytest.fixture
def wrong_key() -> str:
    return "wrong_key"


@pytest.fixture
def base_model() -> orm.Mapper[Any]:
    metadata = sa.MetaData()
    return orm.declarative_base(metadata=metadata)  # type: ignore


@pytest.fixture
def orm_async_engine() -> AsyncEngine:
    return create_async_engine("sqlite+aiosqlite:///")


@pytest.fixture
def session_factory(orm_async_engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(orm_async_engine, class_=AsyncSession)


@pytest.fixture
def session(session_factory: async_sessionmaker[AsyncSession]) -> AsyncSession:
    session = session_factory()
    if not isinstance(session, AsyncSession):
        raise TypeError
    return session_factory()


@pytest.fixture
def main_middleware() -> THandler:
    return sa_middleware(SA_DEFAULT_KEY)


@pytest.fixture
def middlewared_app(session_factory: async_sessionmaker[AsyncSession]) -> Application:
    app = web.Application()
    aiohttp_sqlalchemy.setup(app, [sa_bind(session_factory)])
    return app


@pytest.fixture
def mocked_request(middlewared_app: Application) -> Request:
    return make_mocked_request(METH_GET, "/", app=middlewared_app)


@pytest.fixture
def function_handler() -> THandler:
    async def handler(request: Request) -> Response:
        assert isinstance(request, Request)
        return web.json_response()

    return handler


class ClassHandler:
    async def get(self, request: Request) -> Response:
        assert isinstance(request, Request)
        return web.json_response()


class ClassBasedView(web.View):
    async def get(self) -> Response:
        return web.json_response({})
