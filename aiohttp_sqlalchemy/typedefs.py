from aiohttp.web import StreamResponse
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from typing import Awaitable, Callable, Iterable, Tuple, Union


TSessionFactory = Callable[..., AsyncSession]
THandler = Callable[..., Awaitable[StreamResponse]]

TBindTo = Union[str, AsyncEngine, TSessionFactory]
TBinding = Tuple[TSessionFactory, str, bool]
TBindings = Iterable[TBinding]
