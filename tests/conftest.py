from aiohttp import web
import pytest
from sqlalchemy import orm
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

import aiohttp_sqlalchemy
from aiohttp_sqlalchemy import sa_bind, sa_middleware
from aiohttp_sqlalchemy.constants import DEFAULT_KEY


pytest_plugins = 'aiohttp.pytest_plugin'


@pytest.fixture
def sa_session_factory():
    engine = create_async_engine('sqlite+aiosqlite:///')
    return orm.sessionmaker(engine, AsyncSession)


@pytest.fixture
def sa_session(sa_session_factory):
    return sa_session_factory()


@pytest.fixture
def sa_main_middleware():
    return sa_middleware(DEFAULT_KEY)


from aiohttp.hdrs import METH_GET
from aiohttp.test_utils import make_mocked_request

@pytest.fixture
def middlewared_app(sa_session_factory):
    app = web.Application()
    aiohttp_sqlalchemy.setup(app, [sa_bind(sa_session_factory)])
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
