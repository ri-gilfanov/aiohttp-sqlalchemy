from aiohttp import web
import aiohttp_sqlalchemy
from aiohttp_sqlalchemy import sa_bind
import pytest
from sqlalchemy.ext.asyncio import create_async_engine
from aiohttp_sqlalchemy.exceptions import DuplicateAppKeyError, DuplicateRequestKeyError


def test_aiohttp_sqlalchemy_setup():
    engine = create_async_engine('sqlite+aiosqlite:///')

    app = web.Application()
    with pytest.raises(DuplicateAppKeyError):
        aiohttp_sqlalchemy.setup(app, [
            sa_bind(engine),
            sa_bind(engine),
        ])

    app = web.Application()
    with pytest.raises(DuplicateAppKeyError):
        aiohttp_sqlalchemy.setup(app, [
            sa_bind(engine, 'sa_secondary'),
            sa_bind(engine, 'sa_secondary'),
        ])

    app = web.Application()
    aiohttp_sqlalchemy.setup(app, [
        sa_bind(engine),
        sa_bind(engine, 'sa_secondary'),
    ])
