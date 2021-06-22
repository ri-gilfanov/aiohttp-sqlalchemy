"""AIOHTTP-SQLAlchemy. SQLAlchemy 1.4 / 2.0 support for aiohttp."""
from typing import cast

from aiohttp.web import Application
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import Session, sessionmaker

from aiohttp_sqlalchemy.constants import DEFAULT_KEY, SA_DEFAULT_KEY
from aiohttp_sqlalchemy.decorators import sa_decorator
from aiohttp_sqlalchemy.exceptions import DuplicateAppKeyError, DuplicateRequestKeyError
from aiohttp_sqlalchemy.middlewares import sa_middleware
from aiohttp_sqlalchemy.typedefs import TBinding, TBindings, TBindTo, TSessionFactory
from aiohttp_sqlalchemy.utils import init_db, sa_init_db, sa_session, sa_session_factory
from aiohttp_sqlalchemy.views import (
    SAAbstractView,
    SABaseView,
    SAMixin,
    SAModelMixin,
    SAView,
)

__version__ = "0.17.1"

__all__ = [
    "SA_DEFAULT_KEY",
    "DuplicateAppKeyError",
    "DuplicateRequestKeyError",
    "SABaseView",
    "SAMixin",
    "SAModelMixin",
    "SAView",
    "bind",
    "init_db",
    "sa_decorator",
    "sa_middleware",
    "sa_session",
    "sa_session_factory",
    "setup",
    # Synonyms
    "DEFAULT_KEY",
    "SAAbstractView",
    "sa_bind",
    "sa_init_db",
]


def bind(
    bind_to: TBindTo, key: str = SA_DEFAULT_KEY, *, middleware: bool = True
) -> "TBinding":
    """Function wrapper for binding.

    :param bind_to: target for SQLAlchemy binding. Argument can be database connection
                    url, asynchronous engine or asynchronous session factory.
    :param key: key of SQLAlchemy binding.
    :param middleware: `bool` for enable middleware. True by default.
    """
    if isinstance(bind_to, str):
        bind_to = cast(AsyncEngine, create_async_engine(bind_to))

    if isinstance(bind_to, AsyncEngine):
        bind_to = cast(
            TSessionFactory,
            sessionmaker(
                bind=bind_to,
                class_=AsyncSession,
                expire_on_commit=False,
            ),
        )

    for type_ in (AsyncSession, Engine, Session):
        if isinstance(bind_to, type_):
            msg = f"{type_} is unsupported type of argument `bind_to`."
            raise TypeError(msg)

    if not callable(bind_to):
        msg = f"{bind_to} is unsupported type of argument `bind_to`."
        raise TypeError(msg)

    return bind_to, key, middleware


def setup(app: Application, bindings: "TBindings") -> None:
    """Setup function for SQLAlchemy binding to AIOHTTP application.

    :param app: your AIOHTTP application.
    :param bindings: iterable of `aiohttp_sqlalchemy.bind()` calls.
    """
    for factory, key, middleware in bindings:
        if key in app:
            raise DuplicateAppKeyError(key)

        app[key] = factory

        if middleware:
            app.middlewares.append(sa_middleware(key))


# Synonyms
sa_bind = bind
