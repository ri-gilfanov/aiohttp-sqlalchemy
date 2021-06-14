from aiohttp import web
from aiohttp.hdrs import METH_GET
from aiohttp.test_utils import make_mocked_request
import pytest
from sqlalchemy import orm
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

import aiohttp_sqlalchemy
from aiohttp_sqlalchemy import DEFAULT_KEY, sa_bind, sa_middleware


pytest_plugins = 'aiohttp.pytest_plugin'


@pytest.fixture
def orm_async_engine():
    return create_async_engine('sqlite+aiosqlite:///')


@pytest.fixture
def orm_session_factory(orm_async_engine):
    return orm.sessionmaker(orm_async_engine, AsyncSession)


@pytest.fixture
def orm_session(orm_session_factory):
    return orm_session_factory()


@pytest.fixture
def sa_main_middleware():
    return sa_middleware(DEFAULT_KEY)


@pytest.fixture
def middlewared_app(orm_session_factory):
    app = web.Application()
    aiohttp_sqlalchemy.setup(app, [sa_bind(orm_session_factory)])
    return app

@pytest.fixture
def mocked_request(middlewared_app):
    return make_mocked_request(METH_GET, '/', app=middlewared_app)


async def function_handler(request):
    return web.json_response({})


class ClassHandler:
    async def get(request):
        return web.json_response({})


class ClassBasedView(web.View):
    async def get(self):
        return web.json_response({})
