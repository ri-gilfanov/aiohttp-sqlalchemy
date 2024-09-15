from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from aiohttp_sqlalchemy import (
    SA_DEFAULT_KEY,
    DuplicateRequestKeyError,
    sa_middleware,
)

if TYPE_CHECKING:  # pragma: no cover
    from aiohttp.web import Request

    from aiohttp_sqlalchemy.typedefs import THandler


async def test_duplicate_request_key_error(
    mocked_request: Request,
    function_handler: THandler,
    main_middleware: THandler,
    session: AsyncSession,
) -> None:
    assert mocked_request.get(SA_DEFAULT_KEY) is None
    mocked_request[SA_DEFAULT_KEY] = session
    assert mocked_request.get(SA_DEFAULT_KEY) is session

    with pytest.raises(DuplicateRequestKeyError):
        await main_middleware(mocked_request, function_handler)


async def test_session_factory_not_found(
    mocked_request: Request,
    function_handler: THandler,
    wrong_key: str,
) -> None:
    assert wrong_key not in mocked_request
    with pytest.raises(KeyError):
        await sa_middleware(wrong_key)(mocked_request, function_handler)


async def test_sa_middleware(
    mocked_request: Request,
    function_handler: THandler,
    main_middleware: THandler,
) -> None:
    assert mocked_request.get(SA_DEFAULT_KEY) is None
    await main_middleware(mocked_request, function_handler)
    assert isinstance(mocked_request.get(SA_DEFAULT_KEY), AsyncSession)
