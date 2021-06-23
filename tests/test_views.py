import pytest
from aiohttp.web import Request
from sqlalchemy.ext.asyncio import AsyncSession

from aiohttp_sqlalchemy import SA_DEFAULT_KEY, SABaseView


def test_sa_session(
    mocked_request: Request,
    orm_session: AsyncSession,
) -> None:
    mocked_request[SA_DEFAULT_KEY] = orm_session
    view = SABaseView(mocked_request)
    assert view.sa_session() is orm_session
    with pytest.raises(TypeError):
        view.sa_session('wrong key')
