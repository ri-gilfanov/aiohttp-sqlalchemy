from aiohttp.web import Request, StreamResponse, middleware

from aiohttp_sqlalchemy.constants import SA_DEFAULT_KEY
from aiohttp_sqlalchemy.exceptions import DuplicateRequestKeyError
from aiohttp_sqlalchemy.typedefs import THandler


def sa_middleware(key: str = SA_DEFAULT_KEY) -> THandler:
    """SQLAlchemy asynchronous middleware factory.

    :param key: key of SQLAlchemy binding. Has default.
    """

    @middleware
    async def sa_middleware_(request: Request, handler: THandler) -> StreamResponse:
        if key in request:
            raise DuplicateRequestKeyError(key)

        session_factory = request.config_dict.get(key)
        async with session_factory() as request[key]:
            return await handler(request)

    return sa_middleware_
