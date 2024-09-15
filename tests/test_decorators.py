from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from aiohttp_sqlalchemy import (
    SA_DEFAULT_KEY,
    DuplicateRequestKeyError,
    sa_decorator,
)
from tests.conftest import ClassBasedView, ClassHandler

if TYPE_CHECKING:  # pragma: no cover
    from aiohttp.web import Request

    from aiohttp_sqlalchemy.typedefs import THandler


async def test_duplicate_request_key_error(
    mocked_request: Request,
    session: AsyncSession,
    function_handler: THandler,
) -> None:
    assert mocked_request.get(SA_DEFAULT_KEY) is None
    mocked_request[SA_DEFAULT_KEY] = session
    assert mocked_request.get(SA_DEFAULT_KEY) is session
    with pytest.raises(DuplicateRequestKeyError):
        await sa_decorator()(function_handler)(mocked_request)


async def test_session_factory_not_found(
    mocked_request: Request,
    wrong_key: str,
) -> None:
    assert wrong_key not in mocked_request
    with pytest.raises(KeyError):
        await sa_decorator(wrong_key)(ClassBasedView.get)(mocked_request)


async def test_decorated_class_based_view(mocked_request: Request) -> None:
    assert mocked_request.get(SA_DEFAULT_KEY) is None
    await sa_decorator()(ClassBasedView.get)(mocked_request)
    assert isinstance(mocked_request.get(SA_DEFAULT_KEY), AsyncSession)


async def test_decorated_class_handler(mocked_request: Request) -> None:
    assert mocked_request.get(SA_DEFAULT_KEY) is None
    class_handler = ClassHandler()
    await sa_decorator()(class_handler.get)(mocked_request)
    assert isinstance(mocked_request.get(SA_DEFAULT_KEY), AsyncSession)


async def test_decorated_function_handler(
    mocked_request: Request,
    function_handler: THandler,
) -> None:
    assert mocked_request.get(SA_DEFAULT_KEY) is None
    await sa_decorator()(function_handler)(mocked_request)
    assert isinstance(mocked_request.get(SA_DEFAULT_KEY), AsyncSession)
