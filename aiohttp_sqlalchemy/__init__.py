from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import TYPE_CHECKING
import warnings

from aiohttp_sqlalchemy.constants import DEFAULT_KEY
from aiohttp_sqlalchemy.decorators import sa_decorator
from aiohttp_sqlalchemy.exceptions import DuplicateAppKeyError, DuplicateRequestKeyError
from aiohttp_sqlalchemy.middlewares import sa_middleware
from aiohttp_sqlalchemy.views import SABaseView, SAView


if TYPE_CHECKING:
    from aiohttp.web import Application
    from typing import Callable, Iterable, Union, Tuple

    TSessionFactory = Callable[..., AsyncSession]
    TSABinding = Tuple[TSessionFactory, str, bool]


__version__ = '0.8.0'

__all__ = ['DuplicateAppKeyError', 'DuplicateRequestKeyError', 'SABaseView',
           'sa_bind', 'sa_decorator', 'sa_middleware', 'SAView', 'setup',]


def sa_bind(factory: 'TSessionFactory', key: str = DEFAULT_KEY, *,
            middleware: bool = True) -> 'TSABinding':
    """ Session factory wrapper for binding in setup function. """

    if isinstance(factory, AsyncEngine):
        msg = (
            "`AsyncEngine` type is deprecated in `sa_bind()` signature. "
            "Use `sessionmaker(engine, AsyncSession)` or custom session "
            "factory returning `AsyncSession` instance."
        )
        warnings.warn(msg, stacklevel=2)
        factory = sessionmaker(factory, AsyncSession)

    return factory, key, middleware


def setup(app: 'Application', bindings: 'Iterable[TSABinding]'):
    """ Setup function for binding SQLAlchemy engines. """
    for Session, key, middleware in bindings:
        if key in app:
            raise DuplicateAppKeyError(key)

        app[key] = Session

        if middleware:
            app.middlewares.append(sa_middleware(key))
