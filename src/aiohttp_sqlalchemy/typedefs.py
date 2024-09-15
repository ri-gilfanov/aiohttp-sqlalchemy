from typing import Awaitable, Callable, Iterable, Tuple, Union

from aiohttp.web import StreamResponse
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import Session, sessionmaker

THandler = Callable[..., Awaitable[StreamResponse]]
THandlerWrapper = Callable[..., THandler]

TTarget = Union[str, AsyncEngine, sessionmaker[Session]]
TBind = Tuple[sessionmaker[Session], str, bool]
TBinds = Iterable[TBind]
