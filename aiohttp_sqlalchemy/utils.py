from typing import TYPE_CHECKING

from aiohttp_sqlalchemy.constants import SA_DEFAULT_KEY

if TYPE_CHECKING:
    from aiohttp.web import Application, Request
    from sqlalchemy import MetaData
    from sqlalchemy.ext.asyncio import AsyncSession
    from typing import Any


async def init_db(
    app: 'Application',
    metadata: 'MetaData',
    key: str = SA_DEFAULT_KEY,
) -> None:
    session_factory = app.get(key)
    session = session_factory()
    async with session.bind.begin() as connection:
        await connection.run_sync(metadata.create_all)


async def sa_init_db(
    app: 'Application',
    metadata: 'MetaData',
    key: str = SA_DEFAULT_KEY,
) -> None:
    await init_db(app, metadata, key)


def sa_session(request: 'Request', key: str = SA_DEFAULT_KEY) -> 'AsyncSession':
    return request[key]
