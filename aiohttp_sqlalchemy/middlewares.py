from __future__ import annotations

from typing import TYPE_CHECKING

from aiohttp.web import Request, StreamResponse, middleware

from aiohttp_sqlalchemy.constants import SA_DEFAULT_KEY
from aiohttp_sqlalchemy.exceptions import DuplicateRequestKeyError

if TYPE_CHECKING:  # pragma: no cover
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

        if session_factory := request.config_dict.get(key):
            async with session_factory() as request[key]:
                return await handler(request)
        else:
            msg = (
                f"Session factory not found by {key}."
                "Check `aiohttp_sqlalchemy.setup()`."
            )
            raise KeyError(msg)

    return sa_middleware_
