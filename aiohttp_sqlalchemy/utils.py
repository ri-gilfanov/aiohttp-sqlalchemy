from typing import TYPE_CHECKING, cast

from aiohttp.web import Application, Request
from sqlalchemy.ext.asyncio import AsyncSession

from aiohttp_sqlalchemy.constants import SA_DEFAULT_KEY

if TYPE_CHECKING:
    from typing import Union

    from sqlalchemy import MetaData

    from aiohttp_sqlalchemy.typedefs import TSessionFactory


async def init_db(
    app: 'Application',
    metadata: 'MetaData',
    key: str = SA_DEFAULT_KEY,
) -> None:
    session_factory = sa_session_factory(app, key)
    async with session_factory() as session:
        async with session.bind.begin() as connection:
            await connection.run_sync(metadata.create_all)


sa_init_db = init_db  # synonym for init_db


def sa_session(
    request: 'Request',
    key: str = SA_DEFAULT_KEY,
) -> 'AsyncSession':
    return request.get(key)


def sa_session_factory(
    source: 'Union[Request, Application]',
    key: str = SA_DEFAULT_KEY,
) -> 'TSessionFactory':
    return cast('TSessionFactory', getattr(source, 'app', source).get(key))
