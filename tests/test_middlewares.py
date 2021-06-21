from typing import TYPE_CHECKING

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from aiohttp_sqlalchemy import SA_DEFAULT_KEY, DuplicateRequestKeyError
from tests.conftest import function_handler

if TYPE_CHECKING:
    from aiohttp.web import Request

    from aiohttp_sqlalchemy.typedefs import THandler


async def test_duplicate_request_key_error(
    sa_main_middleware: "THandler",
    mocked_request: "Request",
    orm_session: AsyncSession,
) -> None:
    assert mocked_request.get(SA_DEFAULT_KEY) is None
    mocked_request[SA_DEFAULT_KEY] = orm_session
    assert mocked_request.get(SA_DEFAULT_KEY) is orm_session

    with pytest.raises(DuplicateRequestKeyError):
        await sa_main_middleware(mocked_request, function_handler)


async def test_sa_middleware(
    sa_main_middleware: "THandler",
    mocked_request: "Request",
) -> None:
    assert mocked_request.get(SA_DEFAULT_KEY) is None
    await sa_main_middleware(mocked_request, function_handler)
    assert isinstance(mocked_request.get(SA_DEFAULT_KEY), AsyncSession)
