from typing import TYPE_CHECKING
from aiohttp_sqlalchemy.constants import DEFAULT_KEY
from aiohttp_sqlalchemy.decorators import sa_decorator
from aiohttp_sqlalchemy.exceptions import DuplicateAppKeyError
from aiohttp_sqlalchemy.middlewares import sa_middleware
from aiohttp_sqlalchemy.views import SAView, SAViewMixin

if TYPE_CHECKING:
    from aiohttp.web import Application
    from sqlalchemy.ext.asyncio import AsyncEngine
    from typing import Iterable, Tuple

    TSAEngine = Tuple[AsyncEngine, str, bool]


__version__ = '0.1b2'


def sa_engine(engine: 'AsyncEngine', key: str = DEFAULT_KEY,
              middleware: bool = True) -> 'TSAEngine':
    """ AsyncEngine wrapper for setup. """
    return engine, key, middleware


def setup(app: 'Application', engines: 'Iterable[TSAEngine]'):
    for engine, key, middleware in engines:
        if key in app:
            raise DuplicateAppKeyError(key)

        app[key] = engine

        if middleware:
            app.middlewares.append(sa_middleware(key))
