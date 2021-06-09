import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from aiohttp_sqlalchemy import DuplicateRequestKeyError, sa_decorator
from tests.conftest import ClassBasedView, ClassHandler, function_handler


async def test_duplicate_request_key_error(mocked_request, sa_session):
    assert mocked_request.get('sa_main') is None
    mocked_request['sa_main'] = sa_session
    assert mocked_request.get('sa_main') is sa_session
    with pytest.raises(DuplicateRequestKeyError):
        await sa_decorator()(function_handler)(mocked_request)


async def test_decorated_class_based_view(mocked_request):
    assert mocked_request.get('sa_main') is None
    await sa_decorator()(ClassBasedView.get)(mocked_request)
    assert isinstance(mocked_request.get('sa_main'), AsyncSession)


async def test_decorated_class_handler(mocked_request):
    assert mocked_request.get('sa_main') is None
    await sa_decorator()(ClassHandler.get)(mocked_request)
    assert isinstance(mocked_request.get('sa_main'), AsyncSession)


async def test_decorated_function_handler(mocked_request):
    assert mocked_request.get('sa_main') is None
    await sa_decorator()(function_handler)(mocked_request)
    assert isinstance(mocked_request.get('sa_main'), AsyncSession)
