import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from aiohttp_sqlalchemy import SA_DEFAULT_KEY, DuplicateRequestKeyError, sa_decorator
from tests.conftest import ClassBasedView, ClassHandler, function_handler


async def test_duplicate_request_key_error(mocked_request, orm_session):
    assert mocked_request.get(SA_DEFAULT_KEY) is None
    mocked_request[SA_DEFAULT_KEY] = orm_session
    assert mocked_request.get(SA_DEFAULT_KEY) is orm_session
    with pytest.raises(DuplicateRequestKeyError):
        await sa_decorator()(function_handler)(mocked_request)


async def test_decorated_class_based_view(mocked_request):
    assert mocked_request.get(SA_DEFAULT_KEY) is None
    await sa_decorator()(ClassBasedView.get)(mocked_request)
    assert isinstance(mocked_request.get(SA_DEFAULT_KEY), AsyncSession)


async def test_decorated_class_handler(mocked_request):
    assert mocked_request.get(SA_DEFAULT_KEY) is None
    class_handler = ClassHandler()
    await sa_decorator()(class_handler.get)(mocked_request)
    assert isinstance(mocked_request.get(SA_DEFAULT_KEY), AsyncSession)


async def test_decorated_function_handler(mocked_request):
    assert mocked_request.get(SA_DEFAULT_KEY) is None
    await sa_decorator()(function_handler)(mocked_request)
    assert isinstance(mocked_request.get(SA_DEFAULT_KEY), AsyncSession)
