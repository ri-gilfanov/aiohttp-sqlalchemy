from typing import Awaitable, Callable, Iterable, Tuple, Union

from aiohttp.web import StreamResponse
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import sessionmaker

THandler = Callable[..., Awaitable[StreamResponse]]
THandlerWrapper = Callable[..., THandler]

TTarget = Union[str, AsyncEngine, sessionmaker]
TBind = Tuple[sessionmaker, str, bool]
TBinds = Iterable[TBind]
