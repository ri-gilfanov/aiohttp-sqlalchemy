from typing import Awaitable, Callable, Iterable, Tuple, Union

from aiohttp.web import StreamResponse
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

THandler = Callable[..., Awaitable[StreamResponse]]
THandlerWrapper = Callable[..., THandler]
TSessionFactory = Callable[..., AsyncSession]

TTarget = Union[str, AsyncEngine, TSessionFactory]
TBind = Tuple[TSessionFactory, str, bool]
TBinds = Iterable[TBind]
