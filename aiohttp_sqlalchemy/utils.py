from typing import TYPE_CHECKING

from aiohttp_sqlalchemy.constants import DEFAULT_KEY

if TYPE_CHECKING:
    from aiohttp.web import Request
    from sqlalchemy.ext.asyncio import AsyncSession


def sa_session(request: 'Request', key: str = DEFAULT_KEY) -> 'AsyncSession':
    return request[key]
