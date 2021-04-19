from aiohttp.web import middleware, View
from aiohttp.abc import AbstractView
from asyncio import iscoroutinefunction
from functools import wraps
from sqlalchemy.ext.asyncio import AsyncSession
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aiohttp.web import Application, Request, StreamResponse
    from sqlalchemy.ext.asyncio import AsyncEngine
    from typing import Callable, Iterable, Tuple


__version__ = '0.1a4'


def sa_decorator(key: str = 'sa_main'):
    def wrapper(handler):
        @wraps(handler)
        async def wrapped(*args, **kwargs):
            # Class based view decorating
            if isinstance(args[0], AbstractView):
                request = args[0].request
                async with AsyncSession(request.app[key]) as request[key]:
                    return await handler(*args, **kwargs)

            # Coroutine function decorating
            elif iscoroutinefunction(handler):
                request = args[0]
                async with AsyncSession(request.app[key]) as request[key]:
                    return await handler(*args, **kwargs)

            else:
                raise TypeError('Unsupported handler type')

        return wrapped
    return wrapper


def sa_middleware(key: str = 'sa_main') -> 'Callable':
    @middleware
    async def sa_middleware_(request: 'Request', handler: 'Callable') -> 'StreamResponse':
        async with AsyncSession(request.app[key]) as request[key]:
            return await handler(request)
    return sa_middleware_


def sa_engine(engine: 'AsyncEngine', key: str = 'sa_main') -> 'Tuple[AsyncEngine, str]':
    return engine, key


def setup(app: 'Application', engines: 'Iterable[Tuple[AsyncEngine, str]]'):
    for engine, key in engines:
        if key in app:
            raise ValueError(
                f'Duplicated app key `{key}`. Check `engines` argument'
                f'in `aiohttp_sqlalchemy.setup()` call.')
        app[key] = engine


class SAViewMixin:
    request: 'Request'

    @property
    def sa_main(self) -> 'AsyncEngine':
        return self.request['sa_main']


class SAView(View, SAViewMixin):
    pass
