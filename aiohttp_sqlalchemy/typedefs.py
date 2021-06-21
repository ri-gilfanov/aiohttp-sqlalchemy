from typing import Awaitable, Callable, Iterable, Tuple, Union

from aiohttp.web import StreamResponse
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

TSessionFactory = Callable[..., AsyncSession]
THandler = Callable[..., Awaitable[StreamResponse]]
THandlerWrapper = Callable[..., THandler]

TBindTo = Union[str, AsyncEngine, TSessionFactory]
TBinding = Tuple[TSessionFactory, str, bool]
TBindings = Iterable[TBinding]
