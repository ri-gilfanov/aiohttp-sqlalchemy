from typing import Awaitable, Callable, Iterable, Tuple, Union

from aiohttp.web import StreamResponse
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

THandler = Callable[..., Awaitable[StreamResponse]]
THandlerWrapper = Callable[..., THandler]

TTarget = Union[str, AsyncEngine, async_sessionmaker[AsyncSession]]
TBind = Tuple[async_sessionmaker[AsyncSession], str, bool]
TBinds = Iterable[TBind]
