"""AIOHTTP-SQLAlchemy. SQLAlchemy 1.4 / 2.0 support for aiohttp."""
from aiohttp.web import Application
from aiohttp_things import web_handlers
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import Session, sessionmaker

from aiohttp_sqlalchemy.constants import DEFAULT_KEY, SA_DEFAULT_KEY
from aiohttp_sqlalchemy.decorators import sa_decorator
from aiohttp_sqlalchemy.exceptions import (
    DuplicateAppKeyError,
    DuplicateRequestKeyError,
)
from aiohttp_sqlalchemy.middlewares import sa_middleware
from aiohttp_sqlalchemy.typedefs import TBind, TBinds, TTarget
from aiohttp_sqlalchemy.utils import (
    get_engine,
    get_session,
    get_session_factory,
    init_db,
    sa_init_db,
    sa_session,
    sa_session_factory,
)
from aiohttp_sqlalchemy.web_handlers import (
    ListAddMixin,
    ListDeleteMixin,
    ListEditMixin,
    ListViewMixin,
    OffsetPaginationMixin,
    PrimaryKeyMixin,
    SABaseView,
    SAMixin,
    SAModelMixin,
    SAModelView,
    UnitAddMixin,
    UnitDeleteMixin,
    UnitEditMixin,
    UnitViewMixin,
)

__version__ = '0.34.0'

__all__ = [
    'DEFAULT_KEY',
    'DuplicateAppKeyError',
    'DuplicateRequestKeyError',

    'UnitAddMixin',
    'UnitDeleteMixin',
    'UnitEditMixin',
    'UnitViewMixin',

    'ListAddMixin',
    'ListDeleteMixin',
    'ListEditMixin',
    'ListViewMixin',

    'OffsetPaginationMixin',
    'PrimaryKeyMixin',

    'SABaseView',
    'SA_DEFAULT_KEY',

    'SAModelMixin',

    'SAMixin',
    'SAModelView',
    'bind',
    'get_engine',
    'get_session',
    'get_session_factory',
    'init_db',
    'sa_decorator',
    'sa_middleware',
    'setup',
    'web_handlers',
    # Synonyms
    'DEFAULT_KEY',
    'sa_bind',
    'sa_init_db',
    'sa_session',
    'sa_session_factory',
]


def bind(
    target: TTarget,
    key: str = SA_DEFAULT_KEY,
    *,
    middleware: bool = True,
) -> 'TBind':
    """Function wrapper for binding.

    :param target: argument can be database connection url, asynchronous engine
                   or asynchronous session factory.
    :param key: key of SQLAlchemy binding.
    :param middleware: `bool` for enable middleware. True by default.
    """
    if isinstance(target, str):
        target = create_async_engine(target)

    if isinstance(target, AsyncEngine):
        target = sessionmaker(
            bind=target,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    if isinstance(target, (AsyncSession, Engine, Session)):
        msg = f'{type(target)} is unsupported type of argument `target`.'
        raise TypeError(msg)

    if not callable(target):
        msg = f'{target} is unsupported type of argument `target`.'
        raise TypeError(msg)

    return target, key, middleware


def setup(app: Application, binds: "TBinds") -> None:
    """Setup function for SQLAlchemy binding to AIOHTTP application.

    :param app: your AIOHTTP application.
    :param binds: iterable of `aiohttp_sqlalchemy.bind()` calls.
    """
    for factory, key, middleware in binds:
        if key in app:
            raise DuplicateAppKeyError(key)

        app[key] = factory

        if middleware:
            app.middlewares.append(sa_middleware(key))


# Synonyms
sa_bind = bind
