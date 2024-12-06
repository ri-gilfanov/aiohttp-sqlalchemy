from collections.abc import Awaitable, Iterable
from typing import Callable, Union

from aiohttp.web import StreamResponse
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

THandler = Callable[..., Awaitable[StreamResponse]]
THandlerWrapper = Callable[..., THandler]

TTarget = Union[str, AsyncEngine, async_sessionmaker[AsyncSession]]
TBind = tuple[async_sessionmaker[AsyncSession], str, bool]
TBinds = Iterable[TBind]
