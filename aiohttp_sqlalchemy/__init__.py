"""AIOHTTP-SQLAlchemy. SQLAlchemy 1.4 / 2.0 support for aiohttp."""
import warnings
from typing import Any, cast

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
from aiohttp_sqlalchemy.typedefs import TBind, TBinds, TSessionFactory, TTarget
from aiohttp_sqlalchemy.utils import (
    get_session,
    get_session_factory,
    init_db,
    sa_init_db,
    sa_session,
    sa_session_factory,
)
from aiohttp_sqlalchemy.web_handlers import (
    ItemAddMixin,
    ItemDeleteMixin,
    ItemEditMixin,
    ItemViewMixin,
    ListAddMixin,
    ListDeleteMixin,
    ListEditMixin,
    ListViewMixin,
    OffsetPagination,
    PrimaryKeyMixin,
    SABaseView,
    SAMixin,
    SAModelDeleteMixin,
    SAModelEditMixin,
    SAModelMixin,
    SAModelView,
    SAModelViewMixin,
)

__version__ = '0.30.0'

__all__ = [
    'DEFAULT_KEY',
    'DuplicateAppKeyError',
    'DuplicateRequestKeyError',

    'ItemAddMixin',
    'ItemDeleteMixin',
    'ItemEditMixin',
    'ItemViewMixin',

    'ListAddMixin',
    'ListDeleteMixin',
    'ListEditMixin',
    'ListViewMixin',

    'OffsetPagination',
    'PrimaryKeyMixin',

    'SABaseView',
    'SA_DEFAULT_KEY',

    'SAModelMixin',
    'SAModelDeleteMixin',
    'SAModelEditMixin',
    'SAModelViewMixin',

    'SAItemAddMixin',
    'SAItemDeleteMixin',
    'SAItemEditMixin',
    'SAItemViewMixin',

    'SAListAddMixin',
    'SAListDeleteMixin',
    'SAListEditMixin',
    'SAListViewMixin',

    'SAMixin',
    'SAModelView',
    'SAPrimaryKeyMixin',
    'bind',
    'get_session',
    'get_session_factory',
    'init_db',
    'sa_decorator',
    'sa_middleware',
    'setup',
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
        target = cast(AsyncEngine, create_async_engine(target))

    if isinstance(target, AsyncEngine):
        target = cast(
            TSessionFactory,
            sessionmaker(
                bind=target,
                class_=AsyncSession,
                expire_on_commit=False,
            ),
        )

    for type_ in (AsyncSession, Engine, Session):
        if isinstance(target, type_):
            msg = f'{type_} is unsupported type of argument `target`.'
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


def __getattr__(name: str) -> Any:
    if name == 'views':
        warnings.warn(
            '`views` module is deprecated. '
            'Use `web_handlers` module.',
            DeprecationWarning,
            stacklevel=2,
        )
        return web_handlers

    DEPRECATION_MAP = {
        'SAItemAddMixin': 'ItemAddMixin',
        'SAItemDeleteMixin': 'ItemDeleteMixin',
        'SAItemEditMixin': 'ItemEditMixin',
        'SAItemViewMixin': 'ItemViewMixin',
        'SAListAddMixin': 'ListAddMixin',
        'SAListDeleteMixin': 'ListDeleteMixin',
        'SAListEditMixin': 'ListEditMixin',
        'SAListViewMixin': 'ListViewMixin',
        'SAPrimaryKeyMixin': 'PrimaryKeyMixin',
    }
    if name in DEPRECATION_MAP.keys():
        warnings.warn(
            f'`{name}` is deprecated. '
            f'Use `{DEPRECATION_MAP[name]}`.',
            DeprecationWarning,
            stacklevel=2,
        )
        return getattr(web_handlers, DEPRECATION_MAP[name])
    raise AttributeError(f"module {__name__} has no attribute {name}")
