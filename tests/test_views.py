from aiohttp_sqlalchemy import DEFAULT_KEY, SABaseView


def test_sa_session(mocked_request, sa_session):
    mocked_request[DEFAULT_KEY] = sa_session
    view = SABaseView(mocked_request)
    assert view.sa_session() is sa_session
