from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from typing import cast, TYPE_CHECKING

from aiohttp_sqlalchemy.constants import DEFAULT_KEY
from aiohttp_sqlalchemy.decorators import sa_decorator
from aiohttp_sqlalchemy.exceptions import DuplicateAppKeyError, \
                                          DuplicateRequestKeyError
from aiohttp_sqlalchemy.middlewares import sa_middleware
from aiohttp_sqlalchemy.utils import sa_session
from aiohttp_sqlalchemy.views import SAAbstractView, SABaseView, SAView


if TYPE_CHECKING:
    from aiohttp.web import Application
    from typing import Callable, Iterable, Union, Tuple

    TSessionFactory = Callable[..., AsyncSession]
    TBindTo = Union[str, Callable[..., AsyncSession]]
    TSABinding = Tuple[TSessionFactory, str, bool]


__version__ = '0.12.0'

__all__ = ['DuplicateAppKeyError', 'DuplicateRequestKeyError',
           'SAAbstractView', 'SABaseView', 'sa_bind', 'sa_decorator',
           'sa_middleware', 'sa_session', 'SAView', 'setup',]


def sa_bind(bind_to: 'TBindTo', key: str = DEFAULT_KEY, *,
            middleware: bool = True) -> 'TSABinding':
    """ Session factory wrapper for binding in setup function. """

    if isinstance(bind_to, str):
        bind_to = cast(AsyncEngine, create_async_engine(bind_to))

    if isinstance(bind_to, AsyncEngine):
        bind_to = cast('TSessionFactory', sessionmaker(bind_to, AsyncSession))

    if isinstance(bind_to, Engine):
        msg = 'Synchronous  engine is unsupported argument for `sa_bind()`.'
        raise ValueError(msg)

    if not callable(bind_to):
        msg = 'Session factory must be callable.'
        raise ValueError(msg)

    if not isinstance(bind_to(), AsyncSession):
        msg = 'Session factory must returning `AsyncSession` instance.'
        raise ValueError(msg)

    return bind_to, key, middleware


def setup(app: 'Application', bindings: 'Iterable[TSABinding]') -> None:
    """ Setup function for binding SQLAlchemy engines. """
    for factory, key, middleware in bindings:
        if key in app:
            raise DuplicateAppKeyError(key)

        app[key] = factory

        if middleware:
            app.middlewares.append(sa_middleware(key))
