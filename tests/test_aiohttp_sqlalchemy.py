from aiohttp import web
import aiohttp_sqlalchemy
from aiohttp_sqlalchemy import sa_engine
import pytest
from sqlalchemy.ext.asyncio import create_async_engine
from aiohttp_sqlalchemy.exceptions import DuplicateAppKeyError, DuplicateRequestKeyError


def test_aiohttp_sqlalchemy_setup():
    engine = create_async_engine('sqlite+aiosqlite:///')

    app = web.Application()
    with pytest.raises(DuplicateAppKeyError):
        aiohttp_sqlalchemy.setup(app, [
            sa_engine(engine),
            sa_engine(engine),
        ])

    app = web.Application()
    with pytest.raises(DuplicateAppKeyError):
        aiohttp_sqlalchemy.setup(app, [
            sa_engine(engine, 'sa_secondary'),
            sa_engine(engine, 'sa_secondary'),
        ])

    app = web.Application()
    aiohttp_sqlalchemy.setup(app, [
        sa_engine(engine),
        sa_engine(engine, 'sa_secondary'),
    ])
