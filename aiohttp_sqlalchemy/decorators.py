from functools import wraps
from typing import Any

from aiohttp.abc import AbstractView
from aiohttp.web import StreamResponse

from aiohttp_sqlalchemy.constants import SA_DEFAULT_KEY
from aiohttp_sqlalchemy.exceptions import DuplicateRequestKeyError
from aiohttp_sqlalchemy.typedefs import THandler, THandlerWrapper


def sa_decorator(key: str = SA_DEFAULT_KEY) -> THandlerWrapper:
    """SQLAlchemy asynchronous handler decorator.

    :param key: key of SQLAlchemy binding.
    """

    def wrapper(handler: THandler) -> THandler:
        @wraps(handler)
        async def wrapped(*args: Any, **kwargs: Any) -> StreamResponse:
            request = args[0].request \
                if isinstance(args[0], AbstractView) \
                else args[-1]

            if key in request:
                raise DuplicateRequestKeyError(key)

            # TODO: after dropped Python 3.7
            # if session_factory := request.config_dict.get(key):
            session_factory = request.config_dict.get(key)
            if session_factory:
                async with session_factory() as request[key]:
                    return await handler(*args, **kwargs)
            else:
                raise KeyError(
                    f'Session factory not found by {key}.'
                    'Check `key` argument of `sa_decorator()`'
                    'or arguments of `aiohttp_sqlalchemy.setup()`.'
                )

        return wrapped

    return wrapper
