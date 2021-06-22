from typing import Union, cast

from aiohttp.web import Application, Request
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession

from aiohttp_sqlalchemy.constants import SA_DEFAULT_KEY
from aiohttp_sqlalchemy.typedefs import TSessionFactory


async def init_db(
    app: Application,
    metadata: MetaData,
    key: str = SA_DEFAULT_KEY,
) -> None:
    """Create all tables, indexes and etc.

    :param app: instance of ``aiohttp.web_app.Application``.
    :param metadata: instance of ``sqlalchemy.scql.schema.MetaData``.
    :param key: key of SQLAlchemy binding. Has default.
    """
    session_factory = sa_session_factory(app, key)
    async with session_factory() as session:
        async with session.bind.begin() as connection:
            await connection.run_sync(metadata.create_all)


def sa_session(
    request: Request,
    key: str = SA_DEFAULT_KEY,
) -> AsyncSession:
    """Return ``AsyncSession`` instance.

    :param request: instance of ``aiohttp.web_request.Request``.
    :param key: key of SQLAlchemy binding. Has default.
    """
    if not isinstance(request, Request):
        raise TypeError(f"{request} is not {Request}.")

    session = request.get(key)
    if not isinstance(session, AsyncSession):
        raise TypeError(f"{session} returned by {key} is not {AsyncSession} instance.")

    return session


def sa_session_factory(
    source: Union[Request, Application],
    key: str = SA_DEFAULT_KEY,
) -> TSessionFactory:
    """Return callable object which returns an ``AsyncSession`` instance.

    :param sorce: instance of ``aiohttp.web_request.Request`` or
                  ``aiohttp.web_app.Application``.
    :param key: key of SQLAlchemy binding. Has default.
    """
    return cast(TSessionFactory, getattr(source, "app", source).get(key))


# Synonyms
sa_init_db = init_db
