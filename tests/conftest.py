from typing import cast

import pytest
from aiohttp import web
from aiohttp.hdrs import METH_GET
from aiohttp.test_utils import make_mocked_request
from aiohttp.web import Request, Response
from aiohttp.web_app import Application
from sqlalchemy import orm
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)

import aiohttp_sqlalchemy
from aiohttp_sqlalchemy import SA_DEFAULT_KEY, sa_bind, sa_middleware
from aiohttp_sqlalchemy.typedefs import THandler, TSessionFactory

pytest_plugins = 'aiohttp.pytest_plugin'


@pytest.fixture
def orm_async_engine() -> AsyncEngine:
    return create_async_engine('sqlite+aiosqlite:///')


@pytest.fixture
def orm_session_factory(orm_async_engine: AsyncEngine) -> TSessionFactory:
    return cast(
        TSessionFactory,
        orm.sessionmaker(orm_async_engine, AsyncSession),
    )


@pytest.fixture
def orm_session(orm_session_factory: TSessionFactory) -> AsyncSession:
    return orm_session_factory()


@pytest.fixture
def sa_main_middleware() -> THandler:
    return sa_middleware(SA_DEFAULT_KEY)


@pytest.fixture
def middlewared_app(orm_session_factory: TSessionFactory) -> Application:
    app = web.Application()
    aiohttp_sqlalchemy.setup(app, [sa_bind(orm_session_factory)])
    return app


@pytest.fixture
def mocked_request(middlewared_app: Application) -> 'Request':
    return make_mocked_request(METH_GET, '/', app=middlewared_app)


async def function_handler(request: Request) -> Response:
    return web.json_response({})


class ClassHandler:
    async def get(self, request: Request) -> Response:
        return web.json_response({})


class ClassBasedView(web.View):
    async def get(self) -> Response:
        return web.json_response({})
