"""AIOHTTP-SQLAlchemy. SQLAlchemy 2.0 support for aiohttp."""

from __future__ import annotations

from importlib.metadata import version
from typing import TYPE_CHECKING

from aiohttp_things import web_handlers
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import Session

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

if TYPE_CHECKING:  # pragma: no cover
    from aiohttp.web import Application

__version__ = version(__package__)

__all__ = [
    "DEFAULT_KEY",
    "DEFAULT_KEY",
    "SA_DEFAULT_KEY",
    "DuplicateAppKeyError",
    "DuplicateRequestKeyError",
    "ListAddMixin",
    "ListDeleteMixin",
    "ListEditMixin",
    "ListViewMixin",
    "OffsetPaginationMixin",
    "PrimaryKeyMixin",
    "SABaseView",
    "SAMixin",
    "SAModelMixin",
    "SAModelView",
    "TBind",
    "TBinds",
    "TTarget",
    "UnitAddMixin",
    "UnitDeleteMixin",
    "UnitEditMixin",
    "UnitViewMixin",
    "bind",
    "get_engine",
    "get_session",
    "get_session_factory",
    "init_db",
    "sa_bind",
    "sa_decorator",
    "sa_init_db",
    "sa_middleware",
    "sa_session",
    "sa_session_factory",
    "setup",
    "web_handlers",
]


def bind(
    target: TTarget,
    key: str = SA_DEFAULT_KEY,
    *,
    middleware: bool = True,
) -> TBind:
    """Function wrapper for binding.

    :param target: argument can be database connection url, asynchronous engine
                   or asynchronous session factory.
    :param key: key of SQLAlchemy binding.
    :param middleware: `bool` for enable middleware. True by default.
    """
    if isinstance(target, str):
        target = create_async_engine(target)

    if isinstance(target, AsyncEngine):
        target = async_sessionmaker(
            bind=target,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    if isinstance(target, (AsyncSession, Engine, Session)):
        msg = f"{type(target)} is unsupported type of argument `target`."
        raise TypeError(msg)

    if not callable(target):
        msg = f"{target} is unsupported type of argument `target`."
        raise TypeError(msg)

    return target, key, middleware


def setup(app: Application, binds: TBinds) -> None:
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
