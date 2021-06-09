import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from aiohttp_sqlalchemy import DuplicateRequestKeyError, sa_decorator
from aiohttp_sqlalchemy.constants import DEFAULT_KEY
from tests.conftest import ClassBasedView, ClassHandler, function_handler


async def test_duplicate_request_key_error(mocked_request, sa_session):
    assert mocked_request.get(DEFAULT_KEY) is None
    mocked_request[DEFAULT_KEY] = sa_session
    assert mocked_request.get(DEFAULT_KEY) is sa_session
    with pytest.raises(DuplicateRequestKeyError):
        await sa_decorator()(function_handler)(mocked_request)


async def test_decorated_class_based_view(mocked_request):
    assert mocked_request.get(DEFAULT_KEY) is None
    await sa_decorator()(ClassBasedView.get)(mocked_request)
    assert isinstance(mocked_request.get(DEFAULT_KEY), AsyncSession)


async def test_decorated_class_handler(mocked_request):
    assert mocked_request.get(DEFAULT_KEY) is None
    await sa_decorator()(ClassHandler.get)(mocked_request)
    assert isinstance(mocked_request.get(DEFAULT_KEY), AsyncSession)


async def test_decorated_function_handler(mocked_request):
    assert mocked_request.get(DEFAULT_KEY) is None
    await sa_decorator()(function_handler)(mocked_request)
    assert isinstance(mocked_request.get(DEFAULT_KEY), AsyncSession)