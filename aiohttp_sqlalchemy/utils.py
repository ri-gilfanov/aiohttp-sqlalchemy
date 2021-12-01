from typing import Union

from aiohttp.web import Application, Request
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker

from aiohttp_sqlalchemy.constants import SA_DEFAULT_KEY


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
    engine = session_factory.kw.get('bind')
    return engine


def get_session(
    request: Request,
    key: str = SA_DEFAULT_KEY,
) -> AsyncSession:
    """Return `AsyncSession` instance.

    :param request: AIOHTTP request object.
    :param key: key of SQLAlchemy binding.
    """
    if not isinstance(request, Request):
        raise TypeError(f'{request} is not {Request}.')

    session = request.get(key)
    if not isinstance(session, AsyncSession):
        raise TypeError(
            f'{session} returned by {key} is not {AsyncSession} instance.'
        )
    return session


def get_session_factory(
    source: Union[Request, Application],
    key: str = SA_DEFAULT_KEY,
) -> sessionmaker:
    """Return callable object which returns an `AsyncSession` instance.

    :param source: AIOHTTP request object or your AIOHTTP application.
    :param key: key of SQLAlchemy binding.
    """
    if not isinstance(source, (Request, Application)):
        raise TypeError(
            'Arg `source` must be `aiohttp.web.Application` or'
            ' `aiohttp.web.Request`.'
        )
    elif isinstance(source, Request):
        return source.config_dict.get(key)
    return source.get(key)


# Synonyms
sa_init_db = init_db
sa_session = get_session
sa_session_factory = get_session_factory
