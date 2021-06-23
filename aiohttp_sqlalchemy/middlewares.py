from aiohttp.web import Request, StreamResponse, middleware

from aiohttp_sqlalchemy.constants import SA_DEFAULT_KEY
from aiohttp_sqlalchemy.exceptions import DuplicateRequestKeyError
from aiohttp_sqlalchemy.typedefs import THandler


def sa_middleware(key: str = SA_DEFAULT_KEY) -> THandler:
    """SQLAlchemy asynchronous middleware factory.

    :param key: key of SQLAlchemy binding. Has default.
    """

    @middleware
    async def sa_middleware_(
        request: Request,
        handler: THandler,
    ) -> StreamResponse:
        if key in request:
            raise DuplicateRequestKeyError(key)

        # TODO: after dropped Python 3.7
        # if session_factory := request.config_dict.get(key):
        session_factory = request.config_dict.get(key)
        if session_factory:
            async with session_factory() as request[key]:
                return await handler(request)
        else:
            raise KeyError(
                f'Session factory not found by {key}.'
                'Check `aiohttp_sqlalchemy.setup()`.'
            )

    return sa_middleware_
