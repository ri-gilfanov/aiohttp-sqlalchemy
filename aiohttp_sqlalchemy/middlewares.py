from aiohttp.web import middleware
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import TYPE_CHECKING

from aiohttp_sqlalchemy.constants import DEFAULT_KEY
from aiohttp_sqlalchemy.exceptions import DuplicateRequestKeyError

if TYPE_CHECKING:
    from aiohttp.web import Request, StreamResponse
    from typing import Callable


def sa_middleware(key: str = DEFAULT_KEY) -> 'Callable':
    """ SQLAlchemy asynchronous middleware factory. """
    @middleware
    async def sa_middleware_(request: 'Request', handler: 'Callable')\
            -> 'StreamResponse':
        if key in request:
            raise DuplicateRequestKeyError(key)

        Session = request.config_dict.get(key)
        async with Session() as request[key]:
            return await handler(request)

    return sa_middleware_
