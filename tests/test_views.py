from aiohttp_sqlalchemy import SABaseView
from aiohttp_sqlalchemy.constants import DEFAULT_KEY


def test_sa_session(mocked_request, sa_session):
    mocked_request[DEFAULT_KEY] = sa_session
    view = SABaseView(mocked_request)
    assert view.sa_session() is sa_session
