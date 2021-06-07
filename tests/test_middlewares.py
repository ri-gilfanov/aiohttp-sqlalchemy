import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from aiohttp_sqlalchemy.exceptions import DuplicateRequestKeyError
from tests.conftest import function_handler


async def test_duplicate_request_key_error(sa_main_middleware, mocked_request, sa_session):
    assert mocked_request.get('sa_main') is None
    mocked_request['sa_main'] = sa_session
    assert mocked_request.get('sa_main') is sa_session

    with pytest.raises(DuplicateRequestKeyError):
        await sa_main_middleware(mocked_request, function_handler)


async def test_sa_middleware(sa_main_middleware, mocked_request):
    assert mocked_request.get('sa_main') is None
    await sa_main_middleware(mocked_request, function_handler)
    assert isinstance(mocked_request.get('sa_main'), AsyncSession)
