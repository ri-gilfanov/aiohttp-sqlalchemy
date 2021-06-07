from aiohttp import web
import aiohttp_sqlalchemy
from aiohttp_sqlalchemy import sa_bind
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from aiohttp_sqlalchemy.exceptions import DuplicateAppKeyError, DuplicateRequestKeyError


def test_aiohttp_sqlalchemy_setup():
    engine = create_async_engine('sqlite+aiosqlite:///')
    Session = sessionmaker(engine, AsyncSession)

    app = web.Application()
    with pytest.raises(DuplicateAppKeyError):
        aiohttp_sqlalchemy.setup(app, [
            sa_bind(Session),
            sa_bind(Session),
        ])

    app = web.Application()
    with pytest.raises(DuplicateAppKeyError):
        aiohttp_sqlalchemy.setup(app, [
            sa_bind(Session, 'sa_secondary'),
            sa_bind(Session, 'sa_secondary'),
        ])

    app = web.Application()
    aiohttp_sqlalchemy.setup(app, [
        sa_bind(Session),
        sa_bind(Session, 'sa_secondary'),
    ])
