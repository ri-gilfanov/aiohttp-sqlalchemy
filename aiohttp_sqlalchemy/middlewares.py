from aiohttp.web import middleware
from typing import TYPE_CHECKING

from aiohttp_sqlalchemy.constants import SA_DEFAULT_KEY
from aiohttp_sqlalchemy.exceptions import DuplicateRequestKeyError

if TYPE_CHECKING:
    from aiohttp.web import Request, StreamResponse
    from typing import Awaitable, Callable

    THandler = Callable[..., Awaitable[StreamResponse]]


def sa_middleware(key: str = SA_DEFAULT_KEY) -> 'THandler':
    """ SQLAlchemy asynchronous middleware factory. """
    @middleware
    async def sa_middleware_(request: 'Request', handler: 'THandler') \
            -> 'StreamResponse':
        if key in request:
            raise DuplicateRequestKeyError(key)

        session_factory = request.config_dict.get(key)
        async with session_factory() as request[key]:
            return await handler(request)

    return sa_middleware_
