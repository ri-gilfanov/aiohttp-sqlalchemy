from typing import TYPE_CHECKING

from aiohttp_sqlalchemy.constants import DEFAULT_KEY
from aiohttp_sqlalchemy.decorators import sa_decorator
from aiohttp_sqlalchemy.exceptions import DuplicateAppKeyError, DuplicateRequestKeyError
from aiohttp_sqlalchemy.middlewares import sa_middleware
from aiohttp_sqlalchemy.views import SABaseView, SAView, SAViewMixin


if TYPE_CHECKING:
    from aiohttp.web import Application
    from sqlalchemy.ext.asyncio import AsyncEngine
    from typing import Iterable, Tuple

    TSABinding = Tuple[AsyncEngine, str, bool]


__version__ = '0.5.0'

__all__ = ['DuplicateAppKeyError', 'DuplicateRequestKeyError', 'SABaseView',
           'sa_bind', 'sa_decorator', 'sa_middleware', 'SAView',
           'SAViewMixin', 'setup',]


def sa_bind(engine: 'AsyncEngine', key: str = DEFAULT_KEY, *,
            middleware: bool = True) -> 'TSABinding':
    """ AsyncEngine wrapper for binding in setup function. """
    return engine, key, middleware


def setup(app: 'Application', bindings: 'Iterable[TSABinding]'):
    """ Setup function for binding SQLAlchemy engines. """
    for engine, key, middleware in bindings:
        if key in app:
            raise DuplicateAppKeyError(key)

        app[key] = engine

        if middleware:
            app.middlewares.append(sa_middleware(key))
