from typing import Awaitable, Callable, Iterable, Optional, Tuple, Union

from aiohttp.web import StreamResponse
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

THandler = Callable[..., Awaitable[StreamResponse]]
THandlerWrapper = Callable[..., THandler]
TSessionFactory = Callable[..., AsyncSession]
TOptSessionFactory = Optional[TSessionFactory]

TTarget = Union[str, AsyncEngine, TSessionFactory]
TBind = Tuple[TSessionFactory, str, bool]
TBinds = Iterable[TBind]
