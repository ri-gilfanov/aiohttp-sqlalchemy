import pytest
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker

import aiohttp_sqlalchemy


def test_bind_to_url() -> None:
    binding = aiohttp_sqlalchemy.bind("sqlite+aiosqlite:///")
    session_factory = binding[0]
    session = session_factory()
    assert isinstance(session, AsyncSession)


def test_bind_to_async_engine(orm_async_engine: AsyncEngine) -> None:
    binding = aiohttp_sqlalchemy.bind(orm_async_engine)
    session_factory = binding[0]
    session = session_factory()
    assert isinstance(session, AsyncSession)


def test_bind_to_sync_engine() -> None:
    engine = create_engine("sqlite+aiosqlite:///")
    with pytest.raises(ValueError):
        aiohttp_sqlalchemy.bind(engine)


def test_bind_with_ready_session(orm_async_engine: AsyncEngine) -> None:
    session = AsyncSession(orm_async_engine)
    with pytest.raises(ValueError):
        aiohttp_sqlalchemy.bind(session)


def test_bind_with_sync_session(orm_async_engine: AsyncEngine) -> None:
    Session = sessionmaker(orm_async_engine)
    with pytest.raises(ValueError):
        aiohttp_sqlalchemy.bind(Session)


def test_bind_to_async_session_maker(orm_async_engine: AsyncEngine) -> None:
    Session = sessionmaker(orm_async_engine, AsyncSession)
    binding = aiohttp_sqlalchemy.bind(Session)
    Session = binding[0]
    session = Session()
    assert isinstance(session, AsyncSession)
