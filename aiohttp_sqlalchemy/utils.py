from typing import Union, cast

from aiohttp.web import Application, Request
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession

from aiohttp_sqlalchemy.constants import SA_DEFAULT_KEY
from aiohttp_sqlalchemy.typedefs import TOptSessionFactory


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
    session_factory = get_session_factory(app, key)
    if callable(session_factory):
        async with session_factory() as session:
            async with session.bind.begin() as connection:
                await connection.run_sync(metadata.create_all)


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
) -> TOptSessionFactory:
    """Return callable object which returns an `AsyncSession` instance.

    :param source: AIOHTTP request object or your AIOHTTP application.
    :param key: key of SQLAlchemy binding.
    """
    if isinstance(source, Request):
        return cast(TOptSessionFactory, source.config_dict.get(key))
    elif isinstance(source, Application):
        return cast(TOptSessionFactory, source.get(key))
    raise TypeError(
        'Arg `source` must be `Application` or `Request` from `aiohttp.web`.'
    )


# Synonyms
sa_init_db = init_db
sa_session = get_session
sa_session_factory = get_session_factory
