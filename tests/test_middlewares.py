import pytest
from aiohttp.web import Request
from sqlalchemy.ext.asyncio import AsyncSession

from aiohttp_sqlalchemy import (
    SA_DEFAULT_KEY,
    DuplicateRequestKeyError,
    sa_middleware,
)
from aiohttp_sqlalchemy.typedefs import THandler
from tests.conftest import function_handler


async def test_duplicate_request_key_error(
    sa_main_middleware: THandler,
    mocked_request: Request,
    session: AsyncSession,
) -> None:
    assert mocked_request.get(SA_DEFAULT_KEY) is None
    mocked_request[SA_DEFAULT_KEY] = session
    assert mocked_request.get(SA_DEFAULT_KEY) is session

    with pytest.raises(DuplicateRequestKeyError):
        await sa_main_middleware(mocked_request, function_handler)


async def test_session_factory_not_found(mocked_request: Request) -> None:
    with pytest.raises(KeyError):
        await sa_middleware('void')(mocked_request, function_handler)


async def test_sa_middleware(
    sa_main_middleware: THandler,
    mocked_request: Request,
) -> None:
    assert mocked_request.get(SA_DEFAULT_KEY) is None
    await sa_main_middleware(mocked_request, function_handler)
    assert isinstance(mocked_request.get(SA_DEFAULT_KEY), AsyncSession)
