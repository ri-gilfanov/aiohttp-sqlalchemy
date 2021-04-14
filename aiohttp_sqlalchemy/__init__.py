from aiohttp.web import middleware
from aiohttp.abc import AbstractView
from asyncio import iscoroutinefunction
from functools import wraps
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aiohttp.web import Application, Request, Response
    from sqlalchemy.ext.asyncio import AsyncEngine
    from typing import Callable, Iterable, Tuple


__version__ = '0.1a2'


def sa_decorator(key: str = 'sa_main'):
    def wrapper(handler):
        @wraps(handler)
        async def wrapped(*args, **kwargs):
            # Class based view decorating
            if issubclass(handler, AbstractView):
                request = args[0].request
                async with AsyncSession(request.app[key]) as request[key]:
                    return await handler(request)

            # Coroutine function decorating
            elif iscoroutinefunction(handler):
                request = args[0]
                async with AsyncSession(request.app[key]) as request[key]:
                    return await handler(request)

            else:
                raise TypeError('Unsupported handler type')

        return wrapped
    return wrapper


def sa_middleware(key: str = 'sa_main') -> 'Callable':
    @middleware
    async def sa_middleware_(request: 'Request', handler: 'Callable') -> 'Response':
        async with AsyncSession(request.app[key]) as request[key]:
            return await handler(request)
    return sa_middleware_


def sa_engine(key: str = 'sa_main', *args, **kwargs) -> 'Tuple[str, AsyncEngine]':
    return key, create_async_engine(*args, **kwargs)


def setup(app: 'Application', engines: 'Iterable[Tuple[str, AsyncEngine]]'):
    for app_key, engine in engines:
        app[app_key] = engine
