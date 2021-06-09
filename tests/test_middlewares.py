import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from aiohttp_sqlalchemy import DuplicateRequestKeyError
from aiohttp_sqlalchemy.constants import DEFAULT_KEY
from tests.conftest import function_handler


async def test_duplicate_request_key_error(sa_main_middleware, mocked_request, sa_session):
    assert mocked_request.get(DEFAULT_KEY) is None
    mocked_request[DEFAULT_KEY] = sa_session
    assert mocked_request.get(DEFAULT_KEY) is sa_session

    with pytest.raises(DuplicateRequestKeyError):
        await sa_main_middleware(mocked_request, function_handler)


async def test_sa_middleware(sa_main_middleware, mocked_request):
    assert mocked_request.get(DEFAULT_KEY) is None
    await sa_main_middleware(mocked_request, function_handler)
    assert isinstance(mocked_request.get(DEFAULT_KEY), AsyncSession)
