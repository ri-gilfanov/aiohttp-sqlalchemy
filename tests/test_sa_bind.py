from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
import pytest

from aiohttp_sqlalchemy import sa_bind


def test_sa_bind_1():
    binding = sa_bind('sqlite+aiosqlite:///')
    session_factory = binding[0]
    session = session_factory()

    assert isinstance(session, AsyncSession)


def test_bind_to_async_engine(orm_async_engine):
    binding = sa_bind(orm_async_engine)
    session_factory = binding[0]
    session = session_factory()

    assert isinstance(session, AsyncSession)


def test_bind_to_sync_engine():
    engine = create_engine('sqlite+aiosqlite:///')
    with pytest.raises(ValueError):
        sa_bind(engine)


def test_sa_bind_with_ready_session(orm_async_engine):
    session = AsyncSession(orm_async_engine)
    with pytest.raises(ValueError):
        sa_bind(session)


def test_sa_bind_with_sync_session(orm_async_engine):
    session_factory = sessionmaker(orm_async_engine)
    with pytest.raises(ValueError):
        sa_bind(session_factory)


def test_sa_bind_5(orm_async_engine):
    session_factory = sessionmaker(orm_async_engine, AsyncSession)
    binding = sa_bind(session_factory)
    session_factory = binding[0]
    session = session_factory()

    assert isinstance(session, AsyncSession)
