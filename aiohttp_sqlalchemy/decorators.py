from aiohttp.abc import AbstractView
from functools import wraps
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
            print(*args)
            request = args[0].request \
                      if isinstance(args[0], AbstractView) \
                      else args[-1]

            if key in request:
                raise DuplicateRequestKeyError(key)

            Session = request.config_dict.get(key)
            async with Session() as request[key]:
                return await handler(*args, **kwargs)

        return wrapped
    return wrapper
