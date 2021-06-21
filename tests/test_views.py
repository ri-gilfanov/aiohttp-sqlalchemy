from typing import TYPE_CHECKING

from aiohttp_sqlalchemy import SA_DEFAULT_KEY, SABaseView

if TYPE_CHECKING:
    from aiohttp.web import Request
    from sqlalchemy.ext.asyncio import AsyncSession


def test_sa_session(
    mocked_request: 'Request',
    orm_session: 'AsyncSession',
) -> None:
    mocked_request[SA_DEFAULT_KEY] = orm_session
    view = SABaseView(mocked_request)
    assert view.sa_session() is orm_session
