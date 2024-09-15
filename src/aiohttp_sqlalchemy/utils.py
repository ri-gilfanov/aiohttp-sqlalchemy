from __future__ import annotations

from typing import TYPE_CHECKING

from aiohttp.web import Application, Request
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from aiohttp_sqlalchemy.constants import SA_DEFAULT_KEY

if TYPE_CHECKING:  # pragma: no cover
    from sqlalchemy import MetaData


async def init_db(
    app: Application,
    metadata: MetaData,
    key: str = SA_DEFAULT_KEY,
) -> None:
    """Create all tables, indexes and etc.

    :param app: your AIOHTTP application.
    :param metadata: ...
    :param key: key of SQLAlchemy binding.
    """
    engine = await get_engine(app, key)
    async with engine.begin() as connection:
        await connection.run_sync(metadata.create_all)


async def get_engine(
    app: Application,
    key: str = SA_DEFAULT_KEY,
) -> AsyncEngine:
    """Return `AsyncEngine` instance.

    :param app: your AIOHTTP application.
    :param key: key of SQLAlchemy binding.
    """
    session_factory = get_session_factory(app, key)
    return session_factory.kw.get("bind")  # type: ignore


def get_session(
    request: Request,
    key: str = SA_DEFAULT_KEY,
) -> AsyncSession:
    """Return `AsyncSession` instance.

    :param request: AIOHTTP request object.
    :param key: key of SQLAlchemy binding.
    """
    if not isinstance(request, Request):
        msg = f"{request} is not {Request}."
        raise TypeError(msg)

    session = request.get(key)
    if not isinstance(session, AsyncSession):
        msg = f"{session} returned by {key} is not {AsyncSession} instance."
        raise TypeError(msg)
    return session


def get_session_factory(
    source: Request | Application,
    key: str = SA_DEFAULT_KEY,
) -> async_sessionmaker[AsyncSession]:
    """Return callable object which returns an `AsyncSession` instance.

    :param source: AIOHTTP request object or your AIOHTTP application.
    :param key: key of SQLAlchemy binding.
    """
    if not isinstance(source, (Request, Application)):
        msg = (
            "Arg `source` must be `aiohttp.web.Application`" "or `aiohttp.web.Request`."
        )
        raise TypeError(msg)
    if isinstance(source, Request):
        return source.config_dict.get(key)  # type: ignore
    return source.get(key)  # type: ignore


# Synonyms
sa_init_db = init_db
sa_session = get_session
sa_session_factory = get_session_factory
