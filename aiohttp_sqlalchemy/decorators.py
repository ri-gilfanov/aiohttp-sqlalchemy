from aiohttp.abc import AbstractView
from asyncio import iscoroutinefunction
from functools import wraps
from sqlalchemy.ext.asyncio import AsyncSession
from typing import TYPE_CHECKING
from aiohttp_sqlalchemy.constants import DEFAULT_KEY
from aiohttp_sqlalchemy.exceptions import DuplicateRequestKeyError

if TYPE_CHECKING:
    from aiohttp.web import StreamResponse


def sa_decorator(key: str = DEFAULT_KEY):
    """ SQLAlchemy asynchronous handler decorator. """
    def wrapper(handler):
        @wraps(handler)
        async def wrapped(*args, **kwargs) -> 'StreamResponse':
            if isinstance(args[0], AbstractView):
                request = args[0].request
            elif iscoroutinefunction(handler):
                request = args[0]
            else:
                raise TypeError('Unsupported handler type')

            if key in request:
                raise DuplicateRequestKeyError(key)

            async with AsyncSession(request.app[key]) as request[key]:
                return await handler(*args, **kwargs)

        return wrapped
    return wrapper
