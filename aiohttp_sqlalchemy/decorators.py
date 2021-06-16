from aiohttp.abc import AbstractView
from functools import wraps
from typing import TYPE_CHECKING

from aiohttp_sqlalchemy.constants import SA_DEFAULT_KEY
from aiohttp_sqlalchemy.exceptions import DuplicateRequestKeyError

if TYPE_CHECKING:
    from aiohttp.web import Request, StreamResponse
    from typing import Any, Awaitable, Callable, Union, Type

    TDecorated = Callable[[Request], Awaitable[StreamResponse]]
    TResult = Callable[..., Union[Type[AbstractView], TDecorated]]


def sa_decorator(key: str = SA_DEFAULT_KEY) -> 'TResult':
    """ SQLAlchemy asynchronous handler decorator. """
    def wrapper(handler: 'TDecorated') -> 'TDecorated':
        @wraps(handler)
        async def wrapped(*args: 'Any', **kwargs: 'Any') -> 'StreamResponse':
            request = args[0].request \
                      if isinstance(args[0], AbstractView) \
                      else args[-1]

            if key in request:
                raise DuplicateRequestKeyError(key)

            session_factory = request.config_dict.get(key)
            async with session_factory() as request[key]:
                return await handler(*args, **kwargs)

        return wrapped
    return wrapper
