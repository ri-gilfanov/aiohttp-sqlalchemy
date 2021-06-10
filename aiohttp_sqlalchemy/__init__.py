from typing import TYPE_CHECKING

from aiohttp_sqlalchemy.constants import DEFAULT_KEY
from aiohttp_sqlalchemy.decorators import sa_decorator
from aiohttp_sqlalchemy.exceptions import DuplicateAppKeyError, \
                                          DuplicateRequestKeyError
from aiohttp_sqlalchemy.middlewares import sa_middleware
from aiohttp_sqlalchemy.utils import sa_session
from aiohttp_sqlalchemy.views import SAAbstractView, SABaseView, SAView


if TYPE_CHECKING:
    from aiohttp.web import Application
    from sqlalchemy.ext.asyncio import AsyncSession
    from typing import Callable, Iterable, Tuple

    TSessionFactory = Callable[..., AsyncSession]
    TSABinding = Tuple[TSessionFactory, str, bool]


__version__ = '0.11.0'

__all__ = ['DuplicateAppKeyError', 'DuplicateRequestKeyError',
           'SAAbstractView', 'SABaseView', 'sa_bind', 'sa_decorator',
           'sa_middleware', 'sa_session', 'SAView', 'setup',]


def sa_bind(factory: 'TSessionFactory', key: str = DEFAULT_KEY, *,
            middleware: bool = True) -> 'TSABinding':
    """ Session factory wrapper for binding in setup function. """
    return factory, key, middleware


def setup(app: 'Application', bindings: 'Iterable[TSABinding]'):
    """ Setup function for binding SQLAlchemy engines. """
    for factory, key, middleware in bindings:
        if key in app:
            raise DuplicateAppKeyError(key)

        app[key] = factory

        if middleware:
            app.middlewares.append(sa_middleware(key))
