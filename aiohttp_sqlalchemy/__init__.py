from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import TYPE_CHECKING

from aiohttp_sqlalchemy.constants import DEFAULT_KEY
from aiohttp_sqlalchemy.decorators import sa_decorator
from aiohttp_sqlalchemy.exceptions import DuplicateAppKeyError, DuplicateRequestKeyError
from aiohttp_sqlalchemy.middlewares import sa_middleware
from aiohttp_sqlalchemy.views import SABaseView, SAView


if TYPE_CHECKING:
    from aiohttp.web import Application
    from typing import Callable, Iterable, Union, Tuple

    TSessionFactory = Callable[..., AsyncSession]
    TEngineOrFactory = Union[AsyncEngine, TSessionFactory]
    TSABinding = Tuple[TSessionFactory, str, bool]


__version__ = '0.7.0'

__all__ = ['DuplicateAppKeyError', 'DuplicateRequestKeyError', 'SABaseView',
           'sa_bind', 'sa_decorator', 'sa_middleware', 'SAView', 'setup',]


def sa_bind(
    arg: 'TEngineOrFactory', key: str = DEFAULT_KEY, *,
    middleware: bool = True) -> 'TSABinding':
    """ Session factory wrapper for binding in setup function. """

    if isinstance(arg, AsyncEngine):
        arg = sessionmaker(arg, AsyncSession)

    return arg, key, middleware


def setup(app: 'Application', bindings: 'Iterable[TSABinding]'):
    """ Setup function for binding SQLAlchemy engines. """
    for Session, key, middleware in bindings:
        if key in app:
            raise DuplicateAppKeyError(key)

        app[key] = Session

        if middleware:
            app.middlewares.append(sa_middleware(key))
