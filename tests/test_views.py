import pytest
from aiohttp.web import Request
from sqlalchemy.ext.asyncio import AsyncSession

from aiohttp_sqlalchemy import SA_DEFAULT_KEY, SABaseView


def test_sa_session(
    mocked_request: Request,
    session: AsyncSession,
) -> None:
    mocked_request[SA_DEFAULT_KEY] = session
    view = SABaseView(mocked_request)
    assert view.sa_session() is session
    with pytest.raises(TypeError):
        view.sa_session('wrong key')
