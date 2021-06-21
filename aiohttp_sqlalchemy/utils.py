from aiohttp.web import Application, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import TYPE_CHECKING

from aiohttp_sqlalchemy.constants import SA_DEFAULT_KEY

if TYPE_CHECKING:
    from sqlalchemy import MetaData
    from typing import Optional, Union
    from aiohttp_sqlalchemy.typedefs import TSessionFactory


async def init_db(
    app: 'Application',
    metadata: 'MetaData',
    key: str = SA_DEFAULT_KEY,
) -> None:
    session_factory = sa_session_factory(app, key)
    if session_factory:
        async with session_factory() as session:
            async with session.bind.begin() as connection:
                await connection.run_sync(metadata.create_all)
    else:
        raise KeyError('Session factory not found by key')


sa_init_db = init_db  # sa_init_db is synonym for init_db


def sa_session(
    request: 'Request',
    key: str = SA_DEFAULT_KEY,
) -> 'AsyncSession':
    session = request.get(key)
    if isinstance(session, AsyncSession):
        return session
    elif session is None:
        raise KeyError('Session not found by key')
    raise TypeError(f'request[{key}] is not instance of AsyncSession')


def sa_session_factory(
    source: 'Union[Request, Application]',
    key: str = SA_DEFAULT_KEY,
) -> 'Optional[TSessionFactory]':
    if isinstance(source, Request):
        return source.app.get(key)
    elif isinstance(source, Application):
        return source.get(key)
    raise TypeError("Argument `source` has unsupported type")
